import copy
import os
from attrs import define, field

# from dataclasses import dataclass
from typing import Any, List, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.utils.transformations import Transformations

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class ContinuousVariable:
    name: str
    lower_bound: int | float
    upper_bound: int | float
    transformation_type: Optional[str] = None
    units: str = ""
    transformations: Transformations = field(init=False)

    def __attrs_post_init__(self):
        self.transformations = None

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(X)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(X)

    def inverse_transform(self, X_transform: np.ndarray) -> np.ndarray:
        if self.transformation_type == "none":
            return X_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(X_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(X_transform)


@define(kw_only=True)
class CategoricalVariable:
    name: str
    categorical_levels: List[str | int]
    units: str = ""
    transformations: Transformations = field(init=False)

    def enum_to_cat_level(self, X_array: np.ndarray) -> np.ndarray:
        # Converts indexes that are generated using mixed-integer space-filling designs (LHS) to their respective name
        return np.array([self.categorical_levels[int(x)] for x in X_array])


@define
class CategoricalVariableOneHot(CategoricalVariable):
    num_categorical_levels: int = field(init=False)

    def __attrs_post_init__(self):
        self.num_categorical_levels = len(self.categorical_levels)

    def one_hot_encode(self, X: np.ndarray) -> np.ndarray:
        return OneHotEncoder(handle_unknown="ignore", categories=self.categorical_levels).transform(X).toarray()


@define(kw_only=True)
class CategoricalVariableDiscreteValues(CategoricalVariable):
    lower_bound: int | float
    upper_bound: int | float
    transformation_type: Optional[str] = None
    num_categorical_levels: int = field(init=False)

    def __attrs_post_init__(self):
        self.num_categorical_levels = len(self.categorical_levels)
        self.transformations = None

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(X)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(X)

    def inverse_transform(self, X_transform: np.ndarray) -> np.ndarray:
        if self.transformation_type == "none":
            return X_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(X_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(X_transform)

    def value_to_discrete(self, X: np.ndarray) -> np.ndarray:
        # Converts values to their closest discrete value
        X_new = copy.copy(X)
        for index, value in enumerate(X):
            diff = ((self.categorical_levels - value) ** 2) ** 0.5
            diff_min_index = np.argmin(diff)
            X_new[index] = self.categorical_levels[diff_min_index]

        return X_new


@define(kw_only=True)
class CategoricalVariableWithDescriptors(CategoricalVariable):
    descriptor_names: List[str]
    categorical_descriptors: List[Any] | np.ndarray
    transformation_type: Optional[str] = None
    lower_bound: Optional[int | float] = None
    upper_bound: Optional[int | float] = None
    num_categorical_levels: int = field(init=False)
    num_descriptors: int = field(init=False)
    # series: pd.Series = field(init=False)

    def __attrs_post_init__(self):
        self.num_categorical_levels = len(self.categorical_levels)
        if self.lower_bound is None:
            self.lower_bound = []
            descriptor_range = np.ptp(self.categorical_descriptors, axis=0)
            for descriptor, range in zip(np.array(self.categorical_descriptors).T, descriptor_range):
                self.lower_bound.append(descriptor.min() - (range * 0.10))

        if self.upper_bound is None:
            self.upper_bound = []
            descriptor_range = np.ptp(self.categorical_descriptors, axis=0)
            for descriptor, range in zip(np.array(self.categorical_descriptors).T, descriptor_range):
                self.upper_bound.append(descriptor.max() + (range * 0.10))

        self.num_descriptors = (
            len(self.categorical_descriptors)
            if np.array(self.categorical_descriptors).ndim == 1
            else len(self.categorical_descriptors[0])
        )

        # index = pd.MultiIndex.from_tuples(
        #     list(zip(*[[self.name] * self.num_categorical_levels, self.categorical_levels])),
        #     names=["Variable Name", "Categorical Option Name"],
        # )
        # self.series = pd.Series(self.categorical_descriptors.tolist(), name="Descriptors", index=index)

    def name_to_descriptor(self, X: np.ndarray) -> np.ndarray:
        return self.categorical_descriptors[self.categorical_levels.index(X)]

    def name_to_enum(self, X: np.ndarray) -> np.ndarray:
        return np.vstack([self.categorical_levels.index(x) for x in X])

    def enum_to_descriptor(self, X: np.ndarray) -> np.ndarray:
        return np.vstack([self.categorical_descriptors[int(x)] for x in X])

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(X)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the variable instance"
            )

        if self.transformation_type == "none":
            return X
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(X)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(X)

    def inverse_transform(self, X_transform: np.ndarray) -> np.ndarray:
        if self.transformation_type == "none":
            return X_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(X_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(X_transform)


@define
class VariablesList:
    variables: List[ContinuousVariable | CategoricalVariable]
    names: List[str] = field(init=False)
    units: List[str] = field(init=False)
    num_cat_onehot_var: int = field(init=False)
    num_cat_discrete_var: int = field(init=False)
    num_cat_descriptor_var: int = field(init=False)
    num_cat_var: int = field(init=False)
    categorical_levels: List[List[str | int]] = field(init=False)
    num_categorical_levels: int = field(init=False)
    descriptor_names: List[List[str]] = field(init=False)
    categorical_descriptors: List[List[str]] = field(init=False)
    num_descriptors: List[int] = field(init=False)
    lower_bounds: List[int | float] = field(init=False)
    upper_bounds: List[int | float] = field(init=False)
    var_splitter_indexes: List[int] = field(init=False)
    n_var: int = field(init=False)
    # categorical_descriptor_index_range: pd.DataFrame = field(init=False)
    # series: pd.DataFrame = field(init=False)
    continuous_var_names: List[str] = field(init=False)

    def __attrs_post_init__(self):
        self.names = [var.name for var in self.variables]
        self.units = [var.units for var in self.variables]

        self.num_cat_onehot_var = sum(isinstance(var, CategoricalVariableOneHot) for var in self.variables)
        self.num_cat_discrete_var = sum(isinstance(var, CategoricalVariableDiscreteValues) for var in self.variables)
        self.num_cat_descriptor_var = sum(isinstance(var, CategoricalVariableWithDescriptors) for var in self.variables)
        self.num_cat_var = self.num_cat_onehot_var + self.num_cat_discrete_var + self.num_cat_descriptor_var

        self.categorical_levels = [
            var.categorical_levels if not isinstance(var, ContinuousVariable) else None for var in self.variables
        ]
        self.num_categorical_levels = [
            var.num_categorical_levels if not isinstance(var, ContinuousVariable) else 0 for var in self.variables
        ]
        self.descriptor_names = [
            var.descriptor_names if isinstance(var, CategoricalVariableWithDescriptors) else None
            for var in self.variables
        ]
        self.categorical_descriptors = [
            var.categorical_descriptors if isinstance(var, CategoricalVariableWithDescriptors) else None
            for var in self.variables
        ]
        self.num_descriptors = [
            var.num_descriptors if isinstance(var, CategoricalVariableWithDescriptors) else 0 for var in self.variables
        ]

        (self.lower_bounds, self.upper_bounds, self.var_splitter_indexes, categorical_descriptor_index_range,) = (
            [],
            [],
            [],
            [],
        )
        var_counter = 0
        for var_index, var in enumerate(self.variables):
            if isinstance(var, ContinuousVariable):
                self.lower_bounds.append(var.lower_bound)
                self.upper_bounds.append(var.upper_bound)
                var_counter += 1
            elif isinstance(var, CategoricalVariableOneHot):
                var_counter += var.num_categorical_levels
            elif isinstance(var, CategoricalVariableDiscreteValues):
                var_counter += 1
            elif isinstance(var, CategoricalVariableWithDescriptors):
                for lower_value, upper_value in zip(var.lower_bound, var.upper_bound):
                    self.lower_bounds.append(lower_value)
                    self.upper_bounds.append(upper_value)

                categorical_descriptor_index_range.append(
                    [
                        var.name,
                        var_index,
                        var_counter,
                        var_counter + var.num_descriptors,
                    ]
                )
                var_counter += var.num_descriptors
            if var_index + 1 < len(self.variables):
                self.var_splitter_indexes.append(var_counter)

        self.n_var = var_counter
        # if len(categorical_descriptor_index_range) > 0:
        #     self.series = pd.concat(
        #         (var.series for var in self.variables if isinstance(var, CategoricalVariableWithDescriptors))
        #     )

        self.continuous_var_names = []
        for var in self.variables:
            if isinstance(var, ContinuousVariable):
                self.continuous_var_names.append(var.name)
            elif isinstance(var, CategoricalVariableWithDescriptors):
                for descriptor_name in var.descriptor_names:
                    self.continuous_var_names.append(descriptor_name)

    def transform(self, X: np.ndarray, transform_type: Optional[str] = None) -> np.ndarray:
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if not isinstance(var, CategoricalVariableOneHot):
                if var.transformation_type is None:
                    var.transformation_type = transform_type

                if X_split[var_index].shape[1] == 1:
                    X_split[var_index] = var.transform(X_split[var_index]).reshape(-1, 1)
                else:
                    X_split[var_index] = var.transform(X_split[var_index])

        return np.hstack(X_split)

    def transform_only(self, X: np.ndarray) -> np.ndarray:
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if not isinstance(var, CategoricalVariableOneHot):
                if X_split[var_index].shape[1] == 1:
                    X_split[var_index] = var.transform_only(X_split[var_index]).reshape(-1, 1)
                else:
                    X_split[var_index] = var.transform_only(X_split[var_index])

        return np.hstack(X_split)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if not isinstance(var, CategoricalVariableOneHot):
                if X_split[var_index].shape[1] == 1:
                    X_split[var_index] = var.inverse_transform(X_split[var_index]).reshape(-1, 1)
                else:
                    X_split[var_index] = var.inverse_transform(X_split[var_index])

        return np.hstack(X_split)

    def categorical_transform(self, X: np.ndarray) -> np.ndarray:
        X_transform = np.zeros_like(X, dtype=np.object)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableOneHot):
                for index in range(X_transform[:, var_index].shape[0]):
                    X_transform[index, var_index] = var.one_hot_encode(X[index, var_index])
            elif isinstance(var, CategoricalVariableDiscreteValues):
                X_transform[:, var_index] = var.value_to_discrete(X[:, var_index])
            elif isinstance(var, CategoricalVariableWithDescriptors):
                for index in range(X_transform[:, var_index].shape[0]):
                    X_transform[index, var_index] = var.name_to_descriptor(X[index, var_index])
            elif isinstance(var, ContinuousVariable):
                X_transform[:, var_index] = X[:, var_index]

        return np.array([np.hstack(row) for row in X_transform]).astype(float)

    def descriptor_to_name(self, X: np.ndarray) -> np.ndarray:
        # Converts continuous (pseudo-)random values that are generated using space-filling designs (LHS) to their respective descriptor values using shortest normalised euclidean distance
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                cat_name_list = []
                for x in X_split[var_index]:
                    euc_dist = [np.linalg.norm(cat_level - x) for cat_level in np.array(var.categorical_descriptors)]
                    euc_dist_min_index = np.argmin(euc_dist)
                    cat_name_list.append([var.categorical_levels[euc_dist_min_index]])
                X_split[var_index] = np.array(cat_name_list)

        return np.hstack(X_split)

    def categorical_values_euc(self, X: np.ndarray) -> np.ndarray:
        X_split = self.split_var(X)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableDiscreteValues):
                X_split[var_index] = var.value_to_discrete(X_split[var_index])
        X = np.hstack(X_split).astype(np.float)

        if any(isinstance(var, CategoricalVariableWithDescriptors) for var in self.variables):
            X = self.value_to_descriptor(X)

        return X

    def value_to_descriptor(self, X_array: np.ndarray) -> np.ndarray:
        X_split = self.split_var(X_array)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                cat_descriptor_list = []
                for x in X_split[var_index]:
                    euc_dist = [np.linalg.norm(cat_level - x) for cat_level in np.array(var.categorical_descriptors)]
                    euc_dist_min_index = np.argmin(euc_dist)
                    cat_descriptor_list.append(var.categorical_descriptors[euc_dist_min_index])
                # X_split[var_index] = np.array(cat_descriptor_list).reshape(1, -1)
                X_split[var_index] = np.array(cat_descriptor_list)

        return np.hstack(X_split)

    def enum_to_descriptor(self, X_array: np.ndarray) -> np.ndarray:
        # Converts indexes that are generated using mixed-integer space-filling designs (LHS) to their respective descriptor values by matching the index of categorical variable from the initial list provided to descriptors
        X_array_object = X_array.astype(np.object)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                X_array_object[:, var_index] = var.enum_to_descriptor(X_array[:, var_index])

        return X_array_object.astype("float32")

    def name_to_descriptor(self, X_array: np.ndarray) -> np.ndarray:
        # Converts names that are generated using mixed-integer space-filling designs (LHS) to their respective descriptor values by matching the name of categorical variable from the initial list provided to descriptors
        X_array_object = X_array.astype(np.object)
        for var_index, var in enumerate(self.variables):
            if isinstance(var, CategoricalVariableWithDescriptors):
                X_array_object[:, var_index] = var.name_to_descriptor(X_array[:, var_index])

        return X_array_object.astype("float32")

    def reshape_to_2d(self, X_array: np.ndarray) -> np.ndarray:
        return np.hstack(X_array.ravel().tolist()).reshape(X_array.shape[0], self.n_var)

    def split_var(self, X_array: np.ndarray) -> np.ndarray:
        return np.split(X_array, self.var_splitter_indexes, axis=1)
