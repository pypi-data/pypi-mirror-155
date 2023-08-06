import os
from dataclasses import dataclass
from itertools import combinations
from typing import Optional, Tuple

import numpy as np
import torch
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated
from pymoo.core.result import Result
from pymoo.factory import get_reference_directions, get_termination
from pymoo.optimize import minimize
from scipy import spatial

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.acquisition_functions.nsga_improvement.problem_wrapper import NSGAProblemWrapper
from nemo_bo.acquisition_functions.nsga_improvement.unsga3 import UNSGA3
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList
from nemo_bo.opt.samplers import LatinHyperCubeSampling, PoolBased, SampleGenerator
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class NSGAImprovement(AcquisitionFunction):
    # def __init__(self, num_candidates):
    #     self.num_candidates = num_candidates
    num_candidates: int

    def generate_candidates(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        sampler: Optional[SampleGenerator] = None,
        constraints: Optional[ConstraintsList] = None,
        **acq_func_kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        if isinstance(sampler, PoolBased):
            raise NotImplementedError(
                "The PoolBased sampler is incompatible with the NSGAImprovement acquisition function. Please select a different sampler if you wish to continue using this acquisition function. Alternatively, you may use the ExpectedImprovement acquisition function with the PoolBased sampler instead"
            )

        self.exploit_or_explore = acq_func_kwargs.get("exploit_or_explore", "exploit")
        self.pop_size = acq_func_kwargs.get("pop_size")
        self.generations = acq_func_kwargs.get("generations")

        Y = self.remove_nan_rows(Y)

        if self.pop_size is None:
            if self.num_candidates == 1:
                self.pop_size = 200
            elif self.num_candidates == 2:
                self.pop_size = 100
            elif self.num_candidates == 3:
                self.pop_size = 70
            elif self.num_candidates == 4:
                self.pop_size = 40

        if self.generations is None:
            self.generations = 30
            # if self.num_candidates == 1:
            #     self.generations = 50
            # elif self.num_candidates == 2:
            #     self.generations = 30
            # elif self.num_candidates == 3:
            #     self.generations = 30
            # elif self.num_candidates == 4:
            #     self.generations = 30

        if self.exploit_or_explore == "exploit":
            self.generate_pareto(variables, objectives, constraints)
            selected_X, selected_Y = self.hvi(self.res.X, self.res.F, Y, variables, objectives)

            self.reset = False

        if self.exploit_or_explore == "explore" or not self.hvi_search_pass:
            selected_X, selected_Y, total_Y_std = self.highest_uncertainty(variables, objectives, sampler, constraints)

            self.exploit_or_explore = "exploit"
            self.reset = True

        return selected_X, selected_Y

    def generate_pareto(
        self, variables: VariablesList, objectives: ObjectivesList, constraints: ConstraintsList
    ) -> Result:
        """
        Performs the NSGA2 multi-objective opt using the functions and predictor models provided

        Parameters
        ----------
        xl : numpy.ndarray or list for the lower bounds for the variables.
        xu : numpy.ndarray or list for the upper bounds for the variables.
        pop_size : int type for the population size in each iteration in NSGA-II
        generations : int type for the number of iterations in NSGA-II

        Returns
        -------
        res : pymoo.model.result.Result type object that contains all of the information for the predicted non-dominated solutions

        """

        xl = 0
        xu = 1

        ref_dirs = get_reference_directions("energy", objectives.n_obj, self.pop_size * 0.9, seed=1)

        logger.info(f"Performing U-NSGA3 opt")
        algorithm = UNSGA3(ref_dirs, pop_size=self.pop_size)
        problem = NSGAProblemWrapper(xl, xu, variables, objectives, constraints)
        termination = get_termination("n_gen", self.generations)

        # Performs the UNSGA3 opt
        self.res = minimize(problem, algorithm, termination, verbose=True)

        # Correct by * -1 for maximising objectives in NSGA2 opt
        for obj_index, obj in enumerate(objectives.max_bool_dict):
            if objectives.max_bool_dict[obj]:
                self.res.F[:, obj_index] *= -1

        # Un-normalise X values identified by NSGA
        self.res.X = (self.res.X * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))) + np.array(
            variables.lower_bounds
        )

        return self.res

    def hvi(
        self,
        X_nsga: np.ndarray,
        Y_nsga: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Identifies the candidate(s) from the non-dominated solutions from the NSGA2 opt that will produce the highest hypervolume or best improvement in d-metric when combined with the experimental data

        Parameters
        ----------
        X_nsga : numpy.ndarray type object with the variable values for all of the predicted non-dominated solutions
        Y_nsga : numpy.ndarray type object with the objective values for all of the predicted non-dominated solutions
        obj_minmax : 2D numpy.ndarray type of minimum and maximum values for each objective. The minimum value chosen should be slightly less than the expected experimental minimum to ensure accurate hypervolume calculation and pareto front identification
            Example: np.array([[min_yield, max_yield], [min_cost, max_cost]])
        number_of_suggestions : int type for the number of solutions to produce from the hypervolume sorting

        Returns
        -------
        selected_X : numpy.ndarray type object with the variable values for the non-dominated solution(s) that is predicted to produce best hypervolume improvement or best improvement in d-metric
        selected_Y : numpy.ndarray type object with the objectives values for the non-dominated solution(s) that is predicted to produce best hypervolume improvement or best improvement in d-metric

        """
        logger.info(f"Identifying conditions with the largest hypervolume")

        # Construct hvrefs and dmetric refs
        ref_point = self.build_ref_point(objectives.max_bool_dict)

        # finding min_max of full dataset
        sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
        sign_adjusted_Y_nsga = self.Y_norm_minmax_transform(Y_nsga, objectives.bounds, objectives.max_bool_dict)

        # Creates a list of hypervolumes after each candidate(s) that successfully improves the hypervolume
        hv_list = []
        candidates_X_list = []
        candidates_Y_list = []
        X_nsga_combos = list(combinations(X_nsga, self.num_candidates))
        Y_nsga_combos = list(combinations(Y_nsga, self.num_candidates))
        sign_adjusted_Y_nsga_combos = list(combinations(sign_adjusted_Y_nsga, self.num_candidates))
        for x, y, candidates_Y in zip(X_nsga_combos, Y_nsga_combos, sign_adjusted_Y_nsga_combos):
            # Adds the candidate objective values to the experimental data set
            YappF = np.vstack([sign_adjusted_Y, np.array(candidates_Y)])
            # Identifies which data points are non-dominated
            pareto_mask_YappF = is_non_dominated(torch.tensor(YappF, dtype=torch.double))
            # Creates an numpy.ndarray containing the non-dominated points
            pareto_front_YappF = YappF[pareto_mask_YappF]

            # The following are checks to confirm that all new points in the candidates_Y set are on the pareto front
            candidate_in_pareto_counter = 0
            for a in candidates_Y:
                if any((a == b).all() for b in pareto_front_YappF):
                    candidate_in_pareto_counter += 1
                else:
                    break
            # So if all new points in the candidates_Y set are on the pareto front, then it will append the x and y and calculate the predicted hypervolume
            if candidate_in_pareto_counter == len(candidates_Y):
                candidates_X_list.append(x)
                candidates_Y_list.append(y)
                # Calculates the hypervolume
                hv = Hypervolume(ref_point=torch.tensor(ref_point, dtype=torch.double))
                hv_list.append(hv.compute(torch.tensor(pareto_front_YappF, dtype=torch.double)))

        # Selects the variable and objective values of the candidate(s) that produced the largest hypervolume
        # if hv_list is not empty
        if hv_list:
            logger.info("Conditions were successfully selected using hypervolume improvement")
            max_idx = hv_list.index(max(hv_list))
            selected_X = np.array(candidates_X_list[max_idx])
            selected_Y = np.array(candidates_Y_list[max_idx])
            self.hvi_search_pass = True

            if variables.num_cat_descriptor_var > 0:
                selected_X = variables.descriptor_to_name(selected_X)

        else:
            logger.info(
                "Failed to identify a set of conditions that would improve the hypervolume at the desired batch size"
            )
            selected_X = np.array([0])
            selected_Y = np.array([0])
            self.hvi_search_pass = False

        return selected_X, selected_Y

    def highest_uncertainty(
        self,
        variables: VariablesList,
        objectives: ObjectivesList,
        sampler: Optional[SampleGenerator] = None,
        constraints: Optional[ConstraintsList] = None,
        num_new_points: int = 200000,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Function to identify a set of input variables from the variable space that has the highest uncertainty for a predicted output value(s)

        Parameters
        ----------
        xl : 1D numpy.ndarray for the lower bounds for the variables.
        xu : 1D numpy.ndarray for the upper bounds for the variables.
        num_new_points : int type of the number of new sets of input variables to generate. Default: 200,000

        Returns
        -------
        self.uncertainty_dict : dict type containing the outputs relating to the uncertainty of the new data points generated

        """
        logger.info(f"Identifying conditions with the highest uncertainty")

        if sampler is None:
            self.sampler = LatinHyperCubeSampling(num_new_points)
        else:
            self.sampler = sampler

        X_new_points = self.sampler.generate_samples(variables, constraints)

        Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

        # Min_max normalisation of Y standard deviation
        # I think this should be fine to minmax normalise like this
        for obj_index, _ in enumerate(objectives.bounds):
            Y_new_points_stddev[:, obj_index] = Y_new_points_stddev[:, obj_index] / (
                objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
            )

        Y_new_points_stddev_sum = np.sum(Y_new_points_stddev, axis=1).reshape(-1, 1)
        sorting_indices = Y_new_points_stddev_sum[:, -1].argsort()

        X_new_points_sorted = X_new_points[sorting_indices][::-1]

        if variables.num_cat_var > 0:
            X_new_points = variables.categorical_transform(X_new_points).astype("float")
        X_new_points_norm_sorted = (
            (X_new_points[sorting_indices][::-1] - np.array(variables.lower_bounds))
            / (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
        )[sorting_indices][::-1]
        Y_new_points_sorted = Y_new_points[sorting_indices][::-1]
        Y_new_points_stddev_sum_sorted = Y_new_points_stddev_sum[sorting_indices][::-1]

        # 0 index for the highest uncertainty one at the top of the array
        chosen_indices = [0]
        # cosine similarity index of 1.0 for the highest uncertainty one at the top of the array
        cosine_simularity_list = [1.0]
        # Comparing the X_values for the highest uncertainty with every other entry down the sorted X_array
        for index, x in enumerate(X_new_points_norm_sorted):
            cosine_simularity_index = 1 - spatial.distance.cosine(X_new_points_norm_sorted[0], x)
            # Only passes if the cosine similarity index of a given x row is greater than 0.1 different from all of the x's in the list
            if all((((x - cosine_simularity_index) ** 2) ** 0.5) > 0.1 for x in cosine_simularity_list):
                cosine_simularity_list.append(cosine_simularity_index)
                chosen_indices.append(index)

            if len(chosen_indices) == self.num_candidates:
                break

        selected_X = X_new_points_sorted[chosen_indices]
        selected_Y = Y_new_points_sorted[chosen_indices].astype(np.float32)
        total_Y_std = Y_new_points_stddev_sum_sorted[chosen_indices].astype(np.float32)

        logger.info(f"Identified variables with the most uncertain output values")

        return selected_X, selected_Y, total_Y_std
