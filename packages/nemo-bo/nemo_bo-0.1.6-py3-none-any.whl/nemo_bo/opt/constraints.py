import os
from attrs import define, field
from typing import Callable, List, Tuple, Union

import numpy as np
import torch
from torch import Tensor

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class LinearConstraint:
    constraint_type: str
    variables: VariablesList
    features: List[str]
    coefficients: List[int]
    rhs: Union[int, float]
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index = [self.variables.names.index(f) for f in self.features]

    def build_polytope_sampler_constraint(self) -> [Tuple[Tensor, Tensor, float]]:
        """

        Returns
        -------

        """
        return (torch.tensor(self.index), torch.tensor(self.coefficients), self.rhs)

    def build_scipy_constraint(self, add_to_index: int, num_candidates: int) -> Callable:
        """

        Parameters
        ----------
        add_to_index
        num_candidates

        Returns
        -------

        """
        new_index = [i + add_to_index for i in self.index]

        def constraint_fun(x: np.ndarray) -> np.ndarray:
            x_shape = x.shape
            x = x.reshape(num_candidates, -1)
            x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
                self.variables.lower_bounds
            )
            x = x.reshape(x_shape)

            return np.sum(x[new_index] * self.coefficients) - self.rhs

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        """

        Parameters
        ----------
        x

        Returns
        -------

        """
        # Multiply coefficients and rhs by -1 because pymoo uses the less than or equal to inequality operator for its constraints
        if self.constraint_type == "ineq":
            return np.sum(x[:, self.index] * [-coeff for coeff in self.coefficients], axis=1) - (self.rhs * -1)
        else:
            return (np.sum(x[:, self.index] * [-coeff for coeff in self.coefficients], axis=1) - (self.rhs * -1)) ** 2

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        """

        Parameters
        ----------
        X

        Returns
        -------

        """
        if self.constraint_type == "ineq":
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) >= round(float(self.rhs), 4)
        else:
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) == round(float(self.rhs), 4)


@define
class NonLinearConstraint:
    constraint_type: str
    variables: VariablesList
    features: List[str]
    coefficients: List[int]
    powers: List[int]
    rhs: Union[int, float]
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index = [self.variables.names.index(f) for f in self.features]

    def build_polytope_sampler_constraint(self):
        raise TypeError("The polytope sampler cannot be used with non-linear constraints")

    def build_scipy_constraint(self, add_to_index: int, num_candidates: int) -> Callable:
        new_index = [i + add_to_index for i in self.index]

        def constraint_fun(x: np.ndarray) -> np.ndarray:
            x_shape = x.shape
            x = x.reshape(num_candidates, -1)
            x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
                self.variables.lower_bounds
            )
            x = x.reshape(x_shape)

            lhs_eval_list = []
            for i, c, p in zip(new_index, self.coefficients, self.powers):
                lhs_eval_list.append((((x[i]) ** p) * c))

            return sum(lhs_eval_list) - self.rhs

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        # Multiply coefficients and rhs by -1 because pymoo uses the less than or equal to inequality operator for its constraints
        lhs_eval_list = []
        if self.constraint_type == "ineq":
            for i, c, p in zip(self.index, self.coefficients, self.powers):
                lhs_eval_list.append((((x[:, i]) ** p) * -c))

            return np.sum(lhs_eval_list, axis=0) - (self.rhs * -1)

        else:
            for i, c, p in zip(self.index, self.coefficients, self.powers):
                lhs_eval_list.append((((x[:, i]) ** p) * -c))

            return (np.sum(lhs_eval_list, axis=0) - (self.rhs * -1)) ** 2

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        if self.constraint_type == "ineq":
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) >= round(float(self.rhs), 4)
        else:
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) == round(float(self.rhs), 4)


@define
class MaxActiveFeaturesConstraint:
    # Default is greater than or equal to for inequality / or equals for equality
    # Multiply coefficients and rhs by -1 if you want less than or equal to
    variables: VariablesList
    features: List[str]
    max_active: int
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index = [self.variables.names.index(f) for f in self.features]

    def build_polytope_sampler_constraint(self):
        raise TypeError("The polytope sampler cannot be used with max active number of features constraints")
        # return (torch.tensor(self.index), torch.tensor([1] * len(self.index)), self.max_active)

    def build_scipy_constraint(self, add_to_index: int, num_candidates: int) -> Callable:
        new_index = [i + add_to_index for i in self.index]

        def constraint_fun(x: np.ndarray) -> np.ndarray:
            x_shape = x.shape
            x = x.reshape(num_candidates, -1)
            x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
                self.variables.lower_bounds
            )
            x = x.reshape(x_shape)
            x = np.where(x > 0, 1, 0)

            return np.sum(x[new_index] * ([-1] * len(new_index))) - (self.max_active * -1)

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        # Multiply coefficients and rhs by -1 because pymoo uses the less than or equal to inequality operator for its constraints
        X = np.where(x > 0, 1, 0)
        return np.sum(X[:, self.index], axis=1) - self.max_active

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        X = np.where(X > 0, 1, 0)
        return np.sum(X[:, self.index], axis=1) <= self.max_active


@define
class CategoricalConstraint:
    # categorical_levels1 and categorical_levels2 are lists of categories within a features that cannot appear together
    variables: VariablesList
    feature1: str
    feature2: str
    categorical_levels1: List[str]
    categorical_levels2: List[str]
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index1 = [self.variables.names.index(self.feature1)]
        self.index2 = [self.variables.names.index(self.feature2)]

    def build_polytope_sampler_constraint(self):
        raise TypeError("The polytope sampler cannot be used with categorical constraints")

    def build_scipy_constraint(self, add_to_index: int, num_candidates: int) -> Callable:
        def constraint_fun(x: np.ndarray) -> np.ndarray:
            x_shape = x.shape
            x = x.reshape(num_candidates, -1)
            x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
                self.variables.lower_bounds
            )
            x = self.variables.descriptor_to_name(x)
            x = x.reshape(x_shape)

            for row_index, (x1, x2) in enumerate(zip(x[:, self.index1], x[:, self.index2])):
                if x1 in self.categorical_levels1:
                    x[row_index, self.index1] = 1
                if x2 in self.categorical_levels2:
                    x[row_index, self.index2] = 1

            return (x[{self.index1 + add_to_index}] * -1) + (x[{self.index2 + add_to_index}] * -1) - (-1)

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        # Multiply coefficients and rhs by -1 because pymoo uses the less than or equal to inequality operator for its constraints
        x = self.variables.descriptor_to_name(x)

        for row_index, (x1, x2) in enumerate(zip(x[:, self.index1], x[:, self.index2])):
            if x1 in self.categorical_levels1:
                x[row_index, self.index1] = 1
            if x2 in self.categorical_levels2:
                x[row_index, self.index2] = 1

        return np.sum(x[:, [self.index1, self.index2]], axis=1) - 1

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        X = self.variables.descriptor_to_name(X)
        return np.sum((X[:, [self.index1, self.index2]]), axis=1) <= 1


@define
class ConstraintsList:
    constraints: List[Union[LinearConstraint, NonLinearConstraint, MaxActiveFeaturesConstraint, CategoricalConstraint]]
    n_constr: int = field(init=False)

    def __attrs_post_init__(self):
        self.n_constr = len(self.constraints)

    def create_scipy_constraints(self, num_candidates: int) -> List[Tuple[Tensor, Tensor, float]]:
        scipy_constraints = []
        for constr in self.constraints:
            for candidate_number in range(num_candidates):
                if not isinstance(constr, CategoricalConstraint):
                    add_to_index = candidate_number * constr.variables.n_var
                else:
                    add_to_index = candidate_number * len(constr.variables.variables)
                scipy_constraints.append(
                    {
                        "type": constr.constraint_type,
                        "fun": constr.build_scipy_constraint(add_to_index, num_candidates),
                    }
                )

        return scipy_constraints

    def bool_evaluate_constraints(self, X: np.ndarray) -> np.ndarray:
        pass_fail = np.zeros((X.shape[0], self.n_constr))
        for constr_index, constr in enumerate(self.constraints):
            pass_fail[:, constr_index] = constr.bool_evaluate_constraint(X)

        return np.all(pass_fail, axis=1)

    def bool_evaluate_constraints_categorical(self, X: np.ndarray) -> np.ndarray:
        pass_fail = np.zeros((X.shape[0], self.n_constr))
        for constr_index, constr in enumerate(self.constraints):
            X = constr.variables.categorical_transform(X)
            pass_fail[:, constr_index] = constr.bool_evaluate_constraint(X)

        return np.all(pass_fail, axis=1)
