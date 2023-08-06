import os
import random
from attrs import define
from typing import List, Optional, Union

import numpy as np
import torch
from botorch.utils.sampling import get_polytope_samples
from smt.applications.mixed_integer import ENUM, FLOAT, MixedIntegerSamplingMethod
from smt.sampling_methods import LHS, Random

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.variables import ContinuousVariable, VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class SampleGenerator:
    num_new_points: Optional[int] = None


@define
class PolytopeSampling(SampleGenerator):
    def generate_samples(
        self,
        variables: VariablesList,
        constraints: Optional[ConstraintsList] = None,
        seed: int = None,
        n_burnin: int = 10000,
        thinning: int = 32,
    ) -> np.ndarray:
        kwargs = {"seed": seed, "n_burnin": n_burnin, "thinning": thinning}
        if constraints is not None:
            for constr in constraints:
                if constr.constraint_type == "ineq":
                    kwargs["inequality_constraints"] = [constr.build_polytope_sampler_constraint()]
                else:
                    kwargs["equality_constraints"] = [constr.build_polytope_sampler_constraint()]

        samples = (
            get_polytope_samples(
                n=self.num_new_points,
                bounds=torch.tensor([variables.lower_bounds, variables.upper_bounds]),
                **kwargs,
            )
            .cpu()
            .numpy()
        )

        if variables.num_cat_var > 0:
            return variables.descriptor_to_name(samples)
        else:
            return samples


@define
class LatinHyperCubeSampling(SampleGenerator):
    def generate_samples(
        self, variables: VariablesList, constraints: Optional[ConstraintsList] = None, **kwargs
    ) -> np.ndarray:
        """
        Generates a set of data points from latin hypercube sampling

        Parameters
        ----------

        xl : 1D numpy.ndarray for the lower bounds for the variables.
        xu : 1D numpy.ndarray for the upper bounds for the variables.
        num_new_points : int type of the number of new sets of input variables to generate. Default: 200,000

        Returns
        -------
        self.new_points_np : 2D numpy.ndarray type of un_transformed input variables

        """

        xlimits = np.array(
            [
                [var.lower_bound, var.upper_bound] if isinstance(var, ContinuousVariable) else var.categorical_levels
                for var in variables.variables
            ]
        )

        if variables.num_cat_var > 0:
            logger.info(
                f"Generating {self.num_new_points} mixed integer Latin hypercube sampling points in the variable space"
            )
            xtypes = [
                FLOAT if isinstance(var, ContinuousVariable) else (ENUM, var.num_categorical_levels)
                for var in variables.variables
            ]
            lhs = MixedIntegerSamplingMethod(xtypes, xlimits, LHS, random_state=random.randint(0, 1000000))

            X = lhs(self.num_new_points)

            # To do: Improve the implementation for constraints for LHS.
            # Currently this does not sample the available space in a guaranteed LHS manner
            if constraints is not None:
                X = X[constraints.bool_evaluate_constraints(X)]
                while X.shape[0] < self.num_new_points:
                    if X.shape[0] == self.num_new_points - 1:
                        # To last set of variables can some times not be selected when it stays on LHS-type selection and gets stuck in the while loop.
                        # Therefore, the last set of variables is selected randomly
                        sampler = MixedIntegerSamplingMethod(xtypes, xlimits, Random)
                    else:
                        sampler = MixedIntegerSamplingMethod(
                            xtypes,
                            xlimits,
                            LHS,
                            random_state=random.randint(0, 1000000),
                        )

                    remainder = sampler(self.num_new_points - X.shape[0])
                    X = np.vstack((X, remainder))
                    X = X[constraints.bool_evaluate_constraints(X)]
                    X = np.unique(X, axis=0)

            X_object = X.astype(np.object)
            for var_index, var in enumerate(variables.variables):
                if not isinstance(var, ContinuousVariable):
                    X_object[:, var_index] = var.enum_to_cat_level(X[:, var_index])

            return X_object

        else:
            logger.info(
                f"Generating {self.num_new_points} continuous Latin hypercube sampling points in the variable space"
            )
            lhs = LHS(xlimits=xlimits, **kwargs)

            return lhs(self.num_new_points)


@define
class RandomSampling(SampleGenerator):
    def generate_samples(
        self, variables: VariablesList, constraints: Optional[ConstraintsList] = None, **kwargs
    ) -> np.ndarray:
        """
        Generates a set of data points from latin hypercube sampling

        Parameters
        ----------

        xl : 1D numpy.ndarray for the lower bounds for the variables.
        xu : 1D numpy.ndarray for the upper bounds for the variables.
        num_new_points : int type of the number of new sets of input variables to generate. Default: 200,000

        Returns
        -------
        self.new_points_np : 2D numpy.ndarray type of un_transformed input variables

        """

        xlimits = np.array(
            [
                [var.lower_bound, var.upper_bound] if isinstance(var, ContinuousVariable) else var.categorical_levels
                for var in variables.variables
            ]
        )

        if variables.num_cat_var > 0:
            logger.info(f"Generating {self.num_new_points} mixed integer random sampling points in the variable space")
            xtypes = [
                FLOAT if isinstance(var, ContinuousVariable) else (ENUM, var.num_categorical_levels)
                for var in variables.variables
            ]
            sampler = MixedIntegerSamplingMethod(xtypes, xlimits, Random)
            X = sampler(self.num_new_points)

            if constraints is not None:
                X = X[constraints.bool_evaluate_constraints(X)]
                while X.shape[0] < self.num_new_points:
                    remainder = sampler(self.num_new_points - X.shape[0])
                    X = np.vstack((X, remainder))
                    X = X[constraints.bool_evaluate_constraints(X)]
                    X = np.unique(X, axis=0)

            X_object = X.astype(np.object)
            for var_index, var in enumerate(variables.variables):
                if not isinstance(var, ContinuousVariable):
                    X_object[:, var_index] = var.enum_to_cat_level(X[:, var_index])

            return X_object

        else:
            logger.info(f"Generating {self.num_new_points} continuous random sampling points in the variable space")
            sampler = Random(xlimits=xlimits, **kwargs)

            return sampler(self.num_new_points)


@define
class PoolBased:
    X_pool: np.ndarray
    Y_pool: np.ndarray

    def Y_and_update_pool(self, index: Union[int, List[int]]) -> np.ndarray:
        if isinstance(index, int):
            index = [index]

        Y = np.array([self.Y_pool[i] for i in index])

        # Sorts list so that it deletes rows from bottom to top, which ensures that remaining rows higher up in the array do not change index during the for loop
        index.sort(reverse=True)
        for i in index:
            self.X_pool = np.delete(self.X_pool, i, 0)
            self.Y_pool = np.delete(self.Y_pool, i, 0)

        return Y
