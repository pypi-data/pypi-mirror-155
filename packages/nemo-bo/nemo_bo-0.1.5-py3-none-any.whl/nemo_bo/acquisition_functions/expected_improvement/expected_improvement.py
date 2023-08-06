import os
from dataclasses import dataclass
from itertools import combinations
from typing import Optional, Tuple

import numpy as np
import torch
from scipy.optimize import Bounds
from scipy.optimize import minimize as scipy_minimize
from scipy.stats import norm

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.acquisition_functions.expected_improvement.ehvi import ExpectedHypervolumeImprovement
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList
from nemo_bo.opt.samplers import PoolBased, SampleGenerator
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class ExpectedImprovement(AcquisitionFunction):
    # def __init__(self, num_candidates):
    #     self.num_candidates = num_candidates
    num_candidates: int

    def generate_candidates(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        sampler: SampleGenerator | PoolBased,
        constraints: Optional[ConstraintsList] = None,
        **kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        self.sampler = sampler

        Y = self.remove_nan_rows(Y)

        if isinstance(self.sampler, SampleGenerator):
            self.sampler.num_new_points = kwargs.get("num_new_points")
            if self.sampler.num_new_points is None:
                # num_new_points = 5000
                if self.num_candidates == 1:
                    # self.sampler.num_new_points = 500000
                    self.sampler.num_new_points = 500
                elif self.num_candidates == 2:
                    # self.sampler.num_new_points = 1000
                    self.sampler.num_new_points = 50
                elif self.num_candidates == 3:
                    self.sampler.num_new_points = 100
                elif self.num_candidates == 4:
                    # self.sampler.num_new_points = 100 # approx 4 million combinations
                    self.sampler.num_new_points = 75  # approx 1.2 million combinations
                elif self.num_candidates == 5:
                    # self.sampler.num_new_points = 60 # approx 5.5 million combinations
                    self.sampler.num_new_points = 15
        elif isinstance(self.sampler, PoolBased):
            self.sampler.num_new_points = 1
            if self.num_candidates > 4:
                logger.warning(
                    f"The number of suggested candidates is 5 or greater, which is not recommended for pool-based samples with more than 60 samples due to long run times"
                )

        if objectives.n_obj > 1:
            selected_X, selected_Y = self.ehvi(Y, variables, objectives, constraints)

        elif objectives.n_obj == 1:
            self.xi = kwargs.get("xi", 0.01)
            selected_X, selected_Y = self.ei(Y, variables, objectives, constraints)

        self.reset = False

        return selected_X, selected_Y

    def ei(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        logger.info(f"Identifying conditions with the highest expected hypervolume improvement")

        if isinstance(self.sampler, PoolBased):
            logger.info(f"Returning X values from the provided sample pool")
            X_new_points = self.sampler.X_pool
        elif isinstance(self.sampler, SampleGenerator):
            X_new_points = self.sampler.generate_samples(variables, constraints)

        Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

        Y_norm = (Y - objectives.bounds[0]) / (objectives.bounds[1] - objectives.bounds[0])
        Y_new_points_norm = (Y_new_points - objectives.bounds[0]) / (objectives.bounds[1] - objectives.bounds[0])
        # Min_max normalisation of Y standard deviation
        # I think this should be fine to minmax normalise like this
        Y_new_points_stddev_norm = Y_new_points_stddev / (objectives.bounds[1] - objectives.bounds[0])

        logger.info(f"Identifying approximate conditions with the highest expected hypervolume improvement")
        with np.errstate(divide="warn"):
            imp = Y_new_points_norm - np.amax(Y_norm) - self.xi
            Z = imp / Y_new_points_stddev_norm
            ei = imp * norm.cdf(Z) + Y_new_points_stddev_norm * norm.pdf(Z)
            ei[Y_new_points_stddev_norm == 0.0] = 0.0

        index_array = np.arange(X_new_points).reshape(-1, 1)
        concat = np.vstack((X_new_points, Y_new_points, ei)).T
        concat_sorted = concat[concat[:, -1].argsort()]
        index_array_sorted = index_array[concat[:, -1].argsort()]
        X_ei = concat_sorted[: self.num_candidates, :-2]
        Y_ei = concat_sorted[: self.num_candidates, -2].flatten()

        # Writes the indexes of the selected candidates in the sample pool
        if isinstance(self.sampler, PoolBased):
            self.sampler.index = index_array_sorted[: self.num_candidates].flatten().tolist()

            logger.info("Conditions were successfully selected using expected improvement")
            return X_ei, Y_ei

        elif isinstance(self.sampler, SampleGenerator):
            # The objective function to be minimized for the scipy optimize minimize method
            def fun(X_norm):
                X_norm_reshape = X_norm.astype(np.float32).reshape(X_ei.shape)
                X = (X_norm_reshape * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))) + np.array(
                    variables.lower_bounds
                )
                if variables.num_cat_descriptor_var > 0:
                    X = variables.descriptor_to_name(X)

                Y, Y_stddev = objectives.evaluate(X)
                Y_norm = (Y - objectives.bounds[0]) / (objectives.bounds[1] - objectives.bounds[0])
                Y_stddev_norm = Y_new_stddev / (
                    objectives.bounds[1] - objectives.bounds[0]
                )  # I think this should be fine to minmax normalise like this

                with np.errstate(divide="warn"):
                    imp = Y_norm - np.amax(Y_norm) - self.xi
                    Z = imp / Y_stddev_norm
                    ei = imp * norm.cdf(Z) + Y_stddev_norm * norm.pdf(Z)
                    ei[Y_stddev_norm == 0.0] = 0.0

                ei_mean = np.mean(ei)

                return ei_mean

            # Convert the names of categorical variables with their descriptor values
            if variables.num_cat_descriptor_var > 0:
                X_ei = variables.categorical_transform(X_ei)

            # Normalise all variable values against the bounds. This will need to change if one-hot is implemented fully
            X_ei_norm = (X_ei - np.array(variables.lower_bounds)) / (
                np.array(variables.upper_bounds) - np.array(variables.lower_bounds)
            )

            logger.info(f"Optimising the variable location that provides the highest expected improvement")
            if constraints is None:
                method = "L-BFGS-B"
                consts = ()
                options = {"iprint": 99}
            else:
                method = "SLSQP"
                consts = constraints.create_scipy_constraints(self.num_candidates)
                options = {"disp": True}

            res = scipy_minimize(
                fun,
                X_ei_norm,
                method=method,
                jac="3-point",
                bounds=Bounds(
                    lb=np.zeros_like(X_ei_norm).flatten(),
                    ub=np.ones_like(X_ei_norm).flatten(),
                    keep_feasible=True,
                ),
                constraints=consts,
                options=options,
            )

            if res.success == True:
                logger.info(
                    f"Successfully optimised the variable location that provides the highest expected improvement"
                )
                selected_X = res.x.astype(np.float32).reshape(X_ei.shape)
                selected_X = (
                    selected_X * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                ) + np.array(variables.lower_bounds)

                if variables.num_cat_var > 0:
                    selected_X = variables.categorical_values_euc(selected_X)
                if variables.num_cat_descriptor_var > 0:
                    selected_X = variables.descriptor_to_name(selected_X)

                selected_Y, Y_new_stddev = objectives.evaluate(selected_X)

            else:
                logger.warning(
                    f"Optimisation of the variable location that provides the highest expected improvement failed. Will continue with the estimated position"
                )
                selected_X = X_ei
                selected_Y = Y_ei

            logger.info("Conditions were successfully selected using expected improvement")
            return selected_X, selected_Y

    def ehvi(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Identifies the candidate(s) from the non-dominated solutions from the NSGA2 opt that will produce the highest hypervolume or best improvement in d-metric when combined with the experimental data

        Parameters
        ----------
        X_nsga : numpy.ndarray type object with the variable values for all of the predicted non-dominated solutions
        Y_nsga : numpy.ndarray type object with the objective values for all of the predicted non-dominated solutions
        obj_minmax : 2D numpy.ndarray type of minimum and maximum values for each objective. The minimum value chosen should be slightly less than the expected experimental minimum to ensure accurate hypervolume calculation and pareto front identification
            Example: np.array([[min_yield, max_yield], [min_cost, max_cost]])
        num_candidates : int type for the number of solutions to produce from the hypervolume sorting

        Returns
        -------
        selected_X : numpy.ndarray type object with the variable values for the non-dominated solution(s) that is predicted to produce best hypervolume improvement or best improvement in d-metric
        selected_Y : numpy.ndarray type object with the objectives values for the non-dominated solution(s) that is predicted to produce best hypervolume improvement or best improvement in d-metric

        """
        logger.info(f"Identifying conditions with the highest expected hypervolume improvement")

        # Construct hypervolume reference point
        ref_point = self.build_ref_point(objectives.max_bool_dict)

        # logger.info(f"Generating {num_new_points} mixed integer Latin hypercube sampling points in the variable space")
        if isinstance(self.sampler, PoolBased):
            logger.info(f"Returning X values from the provided sample pool")
            X_new_points = self.sampler.X_pool
            index_combos = list(combinations(np.arange(X_new_points.shape[0]), self.num_candidates))
        elif isinstance(self.sampler, SampleGenerator):
            X_new_points = self.sampler.generate_samples(variables, constraints)

        Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

        sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
        sign_adjusted_Y_new_points = self.Y_norm_minmax_transform(
            Y_new_points, objectives.bounds, objectives.max_bool_dict
        )

        # Min_max normalisation of Y standard deviation
        # I think this should be fine to minmax normalise like this
        for obj_index, _ in enumerate(objectives.bounds):
            Y_new_points_stddev[:, obj_index] = Y_new_points_stddev[:, obj_index] / (
                objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
            )

        # Creates a list of expected hypervolume improvements for all combinations of the new Y points
        logger.info(f"Identifying approximate conditions with the highest expected hypervolume improvement")
        ehvi = ExpectedHypervolumeImprovement(
            ref_point=torch.tensor(ref_point, dtype=torch.double),
            Y=torch.tensor(sign_adjusted_Y, dtype=torch.double),
        )
        ehvi_list = []
        X_new_points_combos = list(combinations(X_new_points, self.num_candidates))
        Y_new_points_combos = list(combinations(Y_new_points, self.num_candidates))
        Y_new_points_stddev_combos = list(combinations(Y_new_points_stddev, self.num_candidates))
        sign_adjusted_Y_new_points_combos = list(combinations(sign_adjusted_Y_new_points, self.num_candidates))
        for candidates_Y, candidates_Y_stddev in zip(sign_adjusted_Y_new_points_combos, Y_new_points_stddev_combos):
            try:
                val = ehvi.ehvi_calc(
                    Y_new=torch.tensor(np.array(candidates_Y), dtype=torch.double),
                    Y_new_stddev=torch.tensor(np.array(candidates_Y_stddev), dtype=torch.double),
                )
                ehvi_list.append(val)
            except ValueError:
                ehvi_list.append(torch.tensor(1e-8, dtype=torch.double))

        # Selects the variables and objective values of the candidate(s) that produced the highest expected hypervolume improvement
        max_idx = ehvi_list.index(max(ehvi_list))
        X_ehvi = np.array(X_new_points_combos[max_idx])
        Y_ehvi = np.array(Y_new_points_combos[max_idx])

        # Writes the indexes of the selected candidates in the sample pool
        if isinstance(self.sampler, PoolBased):
            self.sampler.index = list(index_combos[max_idx])

            logger.info("Conditions were successfully selected using expected hypervolume improvement")
            return X_ehvi, Y_ehvi

        elif isinstance(self.sampler, SampleGenerator):
            # The objective function to be minimized for the scipy optimize minimize method
            def fun(X_norm):
                X_norm_reshape = X_norm.astype(np.float32).reshape(X_ehvi.shape)
                X = (X_norm_reshape * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))) + np.array(
                    variables.lower_bounds
                )

                if variables.num_cat_descriptor_var > 0:
                    X = variables.descriptor_to_name(X)

                Y, Y_stddev = objectives.evaluate(X)

                sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
                # Min_max normalisation of Y standard deviation
                # I think this should be fine to minmax normalise like this
                for obj_index, _ in enumerate(objectives.bounds):
                    Y_stddev[:, obj_index] = Y_stddev[:, obj_index] / (
                        objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
                    )

                try:
                    fun_val = -1 * ehvi.ehvi_calc(
                        Y_new=torch.tensor(sign_adjusted_Y, dtype=torch.double),
                        Y_new_stddev=torch.tensor(Y_stddev, dtype=torch.double),
                    )
                except ValueError:
                    fun_val = -1 * torch.tensor(1e-8, dtype=torch.double)

                return fun_val.item()

            # Convert the names of categorical variables with their descriptor values
            if variables.num_cat_descriptor_var > 0:
                X_ehvi = variables.categorical_transform(X_ehvi)

            # Normalise all variable values against the bounds. This will need to change if one-hot is implemented fully
            X_ehvi_norm = (X_ehvi - np.array(variables.lower_bounds)) / (
                np.array(variables.upper_bounds) - np.array(variables.lower_bounds)
            )

            # Performs the scipy optimize minimize method
            logger.info(f"Optimising the variable location that provides the highest expected hypervolume improvement")
            if constraints is None:
                method = "L-BFGS-B"
                consts = ()
                options = {"iprint": 99}
            else:
                method = "SLSQP"
                consts = constraints.create_scipy_constraints(self.num_candidates)
                options = {"disp": True}

            res = scipy_minimize(
                fun,
                X_ehvi_norm,
                method=method,
                jac="3-point",
                bounds=Bounds(
                    lb=np.zeros_like(X_ehvi_norm).flatten(),
                    ub=np.ones_like(X_ehvi_norm).flatten(),
                    keep_feasible=True,
                ),
                constraints=consts,
                options=options,
            )

            if res.fun * -1 > max(ehvi_list).item():
                if res.success == True:
                    logger.info(
                        f"Successfully optimised the variable location that provides the highest expected hypervolume improvement"
                    )
                else:
                    logger.warning(
                        f"Attempts to optimise the variable location that provides the highest expected hypervolume improvement failed to converge but still improved and so will use the new X values"
                    )

                # Transform the optimised X value and calculate the corresponding objective Y values
                selected_X = res.x.astype(np.float32).reshape(X_ehvi.shape)
                selected_X = (
                    selected_X * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                ) + np.array(variables.lower_bounds)

            else:
                logger.warning(
                    f"Attempts to optimise the variable location failed to improve the highest expected hypervolume improvement. Will continue with the estimated X values"
                )

                return X_ehvi, Y_ehvi

            if variables.num_cat_var > 0:
                selected_X = variables.categorical_values_euc(selected_X)
            if variables.num_cat_descriptor_var > 0:
                selected_X = variables.descriptor_to_name(selected_X)

            selected_Y, selected_Y_stddev = objectives.evaluate(selected_X)
            logger.info("Conditions were successfully selected using expected hypervolume improvement")

            return selected_X, selected_Y
