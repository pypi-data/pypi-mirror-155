import os

from attrs import define, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
import nemo_bo.utils.plotter as plotter
from nemo_bo.models.base.available_models import create_predictor_list
from nemo_bo.models.base.base_model import Base_Model
from nemo_bo.opt.variables import VariablesList
from nemo_bo.utils.data_proc import sort_train_test_split_shuffle, remove_nan
from nemo_bo.utils.transformations import Transformations

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define(kw_only=True)
class Objective:
    name: str
    obj_max_bool: bool
    lower_bound: int | float
    upper_bound: int | float
    transformation_type: Optional[str] = None
    units: str = ""

    def transform(self, Y: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the objective instance"
            )

        if self.transformation_type == "none":
            return Y
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(Y)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(Y)

    def transform_only(self, Y: np.ndarray) -> np.ndarray:
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the objective instance"
            )

        if self.transformation_type == "none":
            return Y
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(Y)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(Y)

    def inverse_transform(self, Y_transform: np.ndarray) -> np.ndarray:
        if self.transformation_type == "none":
            return Y_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(Y_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(Y_transform)


@define(kw_only=True)
class RegressionObjective(Objective):
    predictor_type: Optional[str | Base_Model | List[str | Base_Model]] = None
    predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None
    gp_kernel_choices: Optional[list] = None
    model_params: Optional[Dict[str, Any]] = None
    input_predictor_type: str = field(init=False)
    input_predictor_params_dict: Dict[str, Dict[str, Callable]] = field(init=False)
    obj_function: Base_Model = field(init=False)
    permutation_feature_importance: pd.Series = field(init=False)
    transformations: Transformations = field(init=False)

    def __attrs_post_init__(self):
        self.input_predictor_type = self.predictor_type = create_predictor_list(self.predictor_type)
        self.input_predictor_params_dict = self.predictor_params_dict
        self.obj_function = None
        self.permutation_feature_importance = None
        self.transformations = None

    def fit_regressor(
        self, X: np.ndarray, Y: np.ndarray, variables: VariablesList, test_ratio: Optional[float] = 0.2, **kwargs
    ) -> None:
        X, Y = remove_nan(X, Y)

        self.obj_function = self.predictor_type(variables, self)
        self.obj_function.fit(X, Y, test_ratio=test_ratio, **self.model_params, **kwargs)

        # Calculate permutation feature importance
        (
            self.permutation_feature_importance,
            _,
        ) = self.obj_function.permutation_feature_importance_continuous(X, Y)

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        Y_pred, Y_pred_stddev = self.obj_function.predict(X)

        return Y_pred.astype("float"), Y_pred_stddev.astype("float")

    def model_and_hyperparameter_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        model_search_bool: bool,
        test_ratio: Optional[float] = 0.2,
        **kwargs,
    ) -> None:
        X, Y = remove_nan(X, Y)

        if model_search_bool:
            test_loss_list = []
            model_list = []
            model_params_list = []

            # Splits the dataset to create training and test datasets
            if kwargs.get("sort_before_split", True):
                (
                    X_train,
                    X_test,
                    Y_train,
                    Y_test,
                ) = sort_train_test_split_shuffle(X, Y, test_ratio=test_ratio, seed=1)
            else:
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)

            # Performs hyperopt for each predictor type passed into this function and appends each respective best model and hyperparameters
            for predictor_class in self.input_predictor_type:
                predictor_instance = predictor_class(variables, self)
                model, model_params = predictor_instance.hyperparam_opt(
                    X_train, Y_train, test_ratio, predictor_params_dict=self.input_predictor_params_dict, **kwargs
                )
                model_list.append(model)
                model_params_list.append(model_params)

            # Determines the test set prediction accuracy using each optimised predictor type
            for m in model_list:
                Y_test_pred, _ = m.predict(X_test)
                dict = pm.all_performance_metrics(Y_test, Y_test_pred)
                test_loss_list.append(dict["RMSE"])

            # Identifies which predictor type had the most accurate test set prediction
            best_index = test_loss_list.index(min(test_loss_list))
            self.predictor_type = self.input_predictor_type[best_index]
            self.model_params = model_params_list[best_index]

        elif self.obj_function.always_hyperparam_opt:
            # No model search; only hyperopt for the current best predictor type (identified previously)
            predictor_instance = self.predictor_type(variables, self)
            _, self.model_params = predictor_instance.hyperparam_opt(
                X, Y, test_ratio, predictor_params_dict=self.input_predictor_params_dict, **kwargs
            )

        # Re-fits the model but with the complete dataset
        self.fit_regressor(X, Y, variables, test_ratio=test_ratio, **kwargs)

    def parity_plot(self) -> None:

        if self.obj_function.include_validation:
            # Produces a 2D scatter plot showing the parity plot data points, and the x = y line as a line plot
            train_paritydata = self.obj_function.performance_metrics["Train Parity Data"]
            train_rmse = self.obj_function.performance_metrics["Train RMSE"]
            train_r2 = self.obj_function.performance_metrics["Train r2"]
            val_paritydata = self.obj_function.performance_metrics["Validation Parity Data"]
            val_rmse = self.obj_function.performance_metrics["Validation RMSE"]
            val_r2 = self.obj_function.performance_metrics["Validation r2"]

            scatter_parity_data = [train_paritydata, val_paritydata]
            error = [
                self.obj_function.Y_train_error,
                self.obj_function.Y_val_error,
            ]
            max_parity = np.amax(np.vstack([train_paritydata, val_paritydata]))
            min_parity = np.amin(np.vstack([train_paritydata, val_paritydata]))
            # Array for the x = y line in the parity plot
            x_equals_y = [
                [min_parity, min_parity],
                [max_parity, max_parity],
            ]
            scatter_legend = (
                f"Train ({train_paritydata.shape[0]} experiments) (95% CI)",
                f"Test ({val_paritydata.shape[0]} experiments) (95% CI)",
            )
            plot_title = f"{self.obj_function.name} Model {self.name} Parity Plot\nTrain RMSE = {round(train_rmse.astype('float'), 2)} {self.units}, Train r2 = {round(train_r2, 2)}, \nTest RMSE = {round(val_rmse.astype('float'), 2)} {self.units}, Test r2 = {round(val_r2, 2)}"
            path = os.path.join(os.getcwd(), "ML Models", f"{self.obj_function.name}", "Parity Plots")
            if not os.path.exists(path):
                os.makedirs(path)
            output_file = os.path.join(
                path,
                rf"{self.name} {self.obj_function.name} Model Parity Plot, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
            )

        else:
            train_paritydata = self.obj_function.performance_metrics["Parity Data"]
            train_rmse = self.obj_function.performance_metrics["RMSE"]
            train_r2 = self.obj_function.performance_metrics["r2"]
            scatter_parity_data = [train_paritydata]
            error = [self.obj_function.Y_pred_error]
            max_parity = np.amax(np.vstack([train_paritydata]))
            min_parity = np.amin(np.vstack([train_paritydata]))
            # Array for the x = y line in the parity plot
            x_equals_y = [
                [min_parity, min_parity],
                [max_parity, max_parity],
            ]
            scatter_legend = f"Train ({train_paritydata.shape[0]} experiments) (95% CI)"
            plot_title = f"{self.obj_function.name} Model {self.name} Parity Plot\nRMSE = {round(train_rmse.astype('float'), 2)} {self.units}, r2 = {round(train_r2, 2)}"
            path = os.path.join(os.getcwd(), "ML Models", f"{self.obj_function.name}", "Parity Plots")
            if not os.path.exists(path):
                os.makedirs(path)
            output_file = os.path.join(
                path,
                rf"{self.name} {self.obj_function.name} Model Parity Plot, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
            )

        plotter.plot(
            plot_dim="2D",
            scatter_data=scatter_parity_data,
            error=error,
            line_data=x_equals_y,
            scatter_legend=scatter_legend,
            line_legend="x = y",
            xlabel=f"Actual {self.units}",
            ylabel=f"Predicted {self.units}",
            plottitle=plot_title,
            output_file=output_file,
        )
        plt.close()

    def partial_dependence_plot(self, X: np.ndarray) -> Dict[str, pd.DataFrame]:
        partial_dependence_plot_dict = self.obj_function.partial_dependence_plot(X)

        return partial_dependence_plot_dict

    def cv(self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, **kwargs) -> Dict[str, Any]:
        X, Y = remove_nan(X, Y)

        cv_results = self.obj_function.cv(
            X,
            Y,
            self.model_params,
            test_ratio=test_ratio,
            **kwargs,
        )

        return cv_results

    def y_scrambling_cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float = 0.2,
        plot_parity: bool = True,
        inc_error_bars: bool = False,
        **kwargs,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        X, Y = remove_nan(X, Y)

        cv_results, cv_results_y_scrambling = self.obj_function.y_scrambling_cv(
            X,
            Y,
            self.model_params,
            test_ratio=test_ratio,
            plot_parity=plot_parity,
            inc_error_bars=inc_error_bars,
            **kwargs,
        )

        return cv_results, cv_results_y_scrambling


class ObjectiveFunction:
    def __init__(self, obj_function_data: Any):
        self.obj_function_data = obj_function_data

    def evaluate(self, X: np.ndarray, *args, **kwargs) -> None:
        pass


@define(kw_only=True)
class CalculableObjective(Objective):
    obj_function: ObjectiveFunction

    def calculate(self, X: np.ndarray, *args, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        Y = self.obj_function.evaluate(X, *args, **kwargs)
        Y_stddedv = np.zeros_like(Y)

        return Y.astype("float"), Y_stddedv


@define
class ObjectivesList:
    objectives: List[Objective]
    n_obj: int = field(init=False)
    names: List[str] = field(init=False)
    units: List[str] = field(init=False)
    max_bool_dict: Dict[str, bool] = field(init=False)
    bounds: np.ndarray = field(init=False)
    predictor_types: Dict[str, str] = field(init=False)

    def __attrs_post_init__(self):
        self.n_obj = len(self.objectives)
        self.names = [obj.name for obj in self.objectives]
        self.units = [obj.units for obj in self.objectives]
        self.max_bool_dict = {obj.name: obj.obj_max_bool for obj in self.objectives}
        self.bounds = np.array(
            [
                [obj.lower_bound for obj in self.objectives],
                [obj.upper_bound for obj in self.objectives],
            ]
        ).T
        self.predictor_types = {}

    def fit(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        model_search_bool: Optional[bool] = None,
        test_ratio: float = 0.2,
        **kwargs,
    ) -> None:
        if model_search_bool is None:
            model_search_bool = kwargs.get("model_search_bool", False)

        # Fit the ML regression models
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                obj.model_and_hyperparameter_opt(
                    X, Y[:, obj_index], variables, model_search_bool=model_search_bool, test_ratio=test_ratio, **kwargs
                )
                self.predictor_types[self.names[obj_index]] = self.objectives[obj_index].obj_function.name
            else:
                self.predictor_types[self.names[obj_index]] = "calculable objective"

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        Y = np.zeros((X.shape[0], len(self.objectives)), dtype=np.float32)
        Y_stddev = np.zeros_like(Y)
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.predict(X)
            elif isinstance(obj, CalculableObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.calculate(X)

        return Y.astype("float"), Y_stddev.astype("float")

    def parity_plot(self) -> None:
        for obj in self.objectives:
            if isinstance(obj, RegressionObjective):
                obj.parity_plot()

    def partial_dependence_plot(self, X: np.ndarray) -> Dict[str, Dict[str, pd.DataFrame]]:
        partial_dependence_plots_dict = {}
        for obj in self.objectives:
            if isinstance(obj, RegressionObjective):
                partial_dependence_plots_dict[obj.name] = obj.partial_dependence_plot(X)

        return partial_dependence_plots_dict

    def cv(self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, **kwargs) -> Dict[str, Dict[str, Any]]:
        cv_dict = {}
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                cv_dict[obj.name] = obj.cv(X, Y[:, obj_index], test_ratio=test_ratio, **kwargs)

        return cv_dict

    def y_scrambling_cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float = 0.2,
        plot_parity: bool = True,
        inc_error_bars: bool = False,
        **kwargs,
    ) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        cv_dict, cv_y_scrambling_dict = {}, {}
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                cv_dict[obj.name], cv_y_scrambling_dict[obj.name] = obj.y_scrambling_cv(
                    X,
                    Y[:, obj_index],
                    test_ratio=test_ratio,
                    plot_parity=plot_parity,
                    inc_error_bars=inc_error_bars,
                    **kwargs,
                )

        return cv_dict, cv_y_scrambling_dict
