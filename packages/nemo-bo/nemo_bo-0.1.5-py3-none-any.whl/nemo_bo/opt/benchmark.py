import os
from attrs import define, field
from typing import Tuple

import numpy as np

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.opt.objectives import CalculableObjective, ObjectivesList, RegressionObjective
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class Benchmark:
    variables: VariablesList
    objectives: ObjectivesList
    fitted: bool = field(init=False)

    def __attrs_post_init__(self):
        self.fitted = False

    def fit(self, X_groundtruth: np.ndarray, Y_groundtruth: np.ndarray, **kwargs) -> None:
        """

        Parameters
        ----------
        X_groundtruth
        Y_groundtruth

        Returns
        -------

        """
        logger.info(
            "Performing hyperparameter and model search for the best predictor models for use as benchmarkers for the regression objectives"
        )

        # Fit the ML regression models
        self.objectives.fit(
            X_groundtruth,
            Y_groundtruth,
            self.variables,
            model_search_bool=True,
            **kwargs,
        )
        self.fitted = True

        logger.info(
            f"Identified the best predictor models and hyperparameters for the benchmarkers for the regression objectives"
        )

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Parameters
        ----------
        X

        Returns
        -------

        """
        Y = np.zeros((X.shape[0], self.objectives.n_obj), dtype=np.float32)
        Y_stddev = np.zeros_like(Y)
        for obj_index, obj in enumerate(self.objectives.objectives):
            if isinstance(obj, RegressionObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.predict(X)
            elif isinstance(obj, CalculableObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.calculate(X)

        return Y.astype("float"), Y_stddev.astype("float")
