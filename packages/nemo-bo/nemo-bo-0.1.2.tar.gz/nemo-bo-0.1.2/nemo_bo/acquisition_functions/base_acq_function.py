import os
from dataclasses import dataclass
from typing import Dict, List

import numpy as np

import nemo_bo.utils.logger as logging_nemo

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class AcquisitionFunction:
    def build_ref_point(self, max_bool_dict: Dict[str, bool]) -> List[float]:
        ref_point = []
        hv_obj_minmax = np.array([[-0.01, 1.01] for _ in enumerate(max_bool_dict)])
        for obj_index, obj in enumerate(max_bool_dict):
            if max_bool_dict[obj]:
                ref_point.append(hv_obj_minmax[obj_index][0])
            else:
                ref_point.append(hv_obj_minmax[obj_index][1] * -1)

        return ref_point

    def Y_norm_minmax_transform(self, Y, bounds: np.ndarray, max_bool_dict: Dict[str, bool]) -> np.ndarray:
        # Transforms Y using min_max normalisation
        sign_adjusted_Y = np.zeros_like(Y)
        for obj_index, obj in enumerate(max_bool_dict):
            sign_adjusted_Y[:, obj_index] = (Y[:, obj_index] - bounds[obj_index, 0]) / (
                bounds[obj_index, 1] - bounds[obj_index, 0]
            )

            # To determine the pareto front, maximising objective values are left unchanged and minimising objective values are multiplied by -1
            if not max_bool_dict[obj]:
                sign_adjusted_Y[:, obj_index] *= -1

        return sign_adjusted_Y

    def remove_nan_rows(self, Y: np.ndarray) -> np.ndarray:
        # Acquisition functions do not allow for irregular arrays of objective values. Any rows that contains missing values (NaN) are removed
        if Y.ndim == 1:
            return Y[~np.isnan(Y)]
        else:
            return Y[~np.isnan(Y).any(axis=1)]
