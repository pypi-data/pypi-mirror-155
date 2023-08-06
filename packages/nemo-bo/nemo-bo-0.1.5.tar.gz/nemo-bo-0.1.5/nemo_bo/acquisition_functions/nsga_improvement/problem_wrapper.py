from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from pymoo.core.problem import Problem

from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList
from nemo_bo.opt.variables import VariablesList


@dataclass
class NSGAProblemWrapper(Problem):
    """
    Class to be instantiated when defining a problem for the minimise function in NSGA2
    """

    def __init__(
        self,
        xl: int | float | List[int | float],
        xu: int | float | List[int | float],
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: ConstraintsList,
    ):
        """
        Parameters
        ----------
        xl : numpy.ndarray or list or int type for the lower bounds for the variables. If integer all lower bounds are equal (inherited from the Problem class)
        xu : numpy.ndarray or list or int type for the upper bounds for the variables. If integer all upper bounds are equal (inherited from the Problem class)
        n_var : int type for the number of variables (inherited from the Problem class)
        n_obj : int type for the number of objectives (inherited from the Problem class)
        n_constr : int type for the number of constraints (inherited from the Problem class)
        model : Model type object used for evaluating black box objectives in the _evaluate function
        objname_list : list type of the names of the objectives
        obj_max_bool : dict type with the objective names as keys and the values are a boolean, where True correlates to the objective being maximising
        inputchempath : str type of the file path for the input chemicals excel file for the opt
        reactscale : int type for the volume of pump A solution (in mL) used for each reaction
        """
        self.variables = variables
        self.objectives = objectives
        self.constraints = constraints

        n_constr = self.constraints.n_constr if constraints is not None else 0

        super().__init__(
            n_var=self.variables.n_var,
            n_obj=self.objectives.n_obj,
            n_constr=n_constr,
            xl=xl,
            xu=xu,
        )

    def _evaluate(self, X: np.ndarray, out: Dict[str, np.ndarray], **kwargs):
        """
        Function called at line 385 of the pymoo/model/problem.py to calculate the objective values and re-insert them back into NSGA2

        Parameters
        ----------
        X : 1D or 2D numpy.ndarray type of un_transformed input variables
        out : dict type containing the outputs from the NSGA2 for each individual
        kwargs : dict type containing the reaction parameters used for evaluating the objectives for Cost and EcoScore. Initially constructed at line 86 and line 123 of the pymoo/algorithms/genetic_algorithm.py

        Returns
        -------
        out: Appends the out dict with the key "F" containing F, which is a numpy.ndarray with the shape corresponding to the number of individuals defined in X and the number of objectives

        """

        X = (X * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
            self.variables.lower_bounds
        )

        if self.variables.num_cat_descriptor_var > 0:
            F, _ = self.objectives.evaluate(self.variables.descriptor_to_name(X))
        else:
            F, _ = self.objectives.evaluate(X)

        for obj_index, obj in enumerate(self.objectives.max_bool_dict):
            if self.objectives.max_bool_dict[obj]:
                F[:, obj_index] *= -1
        out["F"] = F

        if self.n_constr > 0:
            G = np.zeros((X.shape[0], self.n_constr))
            for index, constr in enumerate(self.constraints.constraints):
                G[:, index] = constr.evaluate_pymoo_constraint(X)
            out["G"] = G
