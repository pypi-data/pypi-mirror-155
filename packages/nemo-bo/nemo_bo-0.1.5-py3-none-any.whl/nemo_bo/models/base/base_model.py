from __future__ import annotations

import copy
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, train_test_split

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
import nemo_bo.utils.plotter as plotter
from nemo_bo.utils.data_proc import *

if TYPE_CHECKING:
    from nemo_bo.opt.objectives import RegressionObjective
    from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


class Base_Model:
    """
    Class to instantiate for fitting GP models
    """

    def __init__(
        self, variables: VariablesList, objective: RegressionObjective, always_hyperparam_opt: bool = True, **kwargs
    ):
        self.variables = variables
        self.input_variables = copy.copy(variables)
        self.objective = objective
        self.input_objective = copy.copy(objective)
        self.always_hyperparam_opt = always_hyperparam_opt
        self.include_validation = None
        self.default_X_transform_type = None
        self.default_Y_transform_type = None
        self.name = None

    def new_instance(self, cls, **params):
        return cls(
            copy.copy(self.input_variables), copy.copy(self.input_objective), self.always_hyperparam_opt, **params
        )

    def fit(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        X_transform: bool = True,
        **params,
    ) -> None:
        pass

    def fit_model(self, *args, **kwargs):
        pass

    def predict(self, X: np.ndarray, X_transform: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        pass

    def cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        if self.include_validation:
            return self.cv_train_val_test(
                X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs
            )
        else:
            return self.cv_train_test(X, Y, model_params, test_ratio=test_ratio, **kwargs)

    def hyperparam_opt(self, *args, **kwargs) -> Dict[str, Any]:
        pass

    def default_params(self, *args, **kwargs) -> Dict[str, Any]:
        pass

    def cv_train_test(
        self, X: np.ndarray, Y: np.ndarray, model_params: Dict[str, Any], test_ratio: float = 0.2, **kwargs
    ) -> Dict[str, Any]:

        self.model_params = model_params

        cv_results = {}
        test_rmse_list = []
        test_r2_list = []
        fold_number = 0

        kf = KFold(n_splits=int(1 / test_ratio))

        # Split the data
        X_temp = copy.copy(X)
        Y_temp = copy.copy(Y)

        remainder = X.shape[0] % int(1 / test_ratio)
        if remainder > 0:
            X_temp = X_temp[: (-1 * remainder)]
            Y_temp = Y_temp[: (-1 * remainder)]

        for train_index, test_index in kf.split(X_temp):
            fold_number += 1
            X_train, X_test = X_temp[train_index], X_temp[test_index]
            Y_train, Y_test = (
                Y_temp[train_index].astype("float"),
                Y_temp[test_index].astype("float"),
            )

            # Create copy for the model
            model = self.new_instance(self.__class__, **kwargs)

            # Transform the data
            model.X_train, model.Y_train, model.X_test, model.Y_test = (
                X_train,
                Y_train,
                X_test,
                Y_test,
            )
            if model.variables.num_cat_var > 0:
                model.X_train = model.variables.categorical_transform(model.X_train).astype("float")
                model.X_test = model.variables.categorical_transform(model.X_test).astype("float")

            model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, Y=model.Y_train)
            model.X_test, model.Y_test = model.transform_only_by_predictor_type(model.X_test, Y=model.Y_test)

            model.fit_model(self.model_params)

            # Make predictions and calculate model performance
            model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
            model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
            model.performance_metrics = pm.all_performance_metrics_train_val(
                Y_train, model.Y_train_pred, Y_test, model.Y_test_pred
            )

            cv_results[f"Fold {fold_number}"] = {
                "Performance Metrics": model.performance_metrics,
                "Model": model.model,
            }
            test_rmse_list.append(model.performance_metrics["Validation RMSE"])
            test_r2_list.append(model.performance_metrics["Validation r2"])

        cv_results["Mean Test RMSE"] = np.mean(test_rmse_list)
        cv_results["Mean Test r2"] = np.mean(test_r2_list)

        logger.info(
            f"Completed {self.name} CV (k = {int(1/test_ratio)}) model checking | Mean Test Loss: {cv_results['Mean Test RMSE']}"
        )

        return cv_results

    def cv_train_val_test(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:

        self.model_params = model_params

        cv_results = {}
        test_rmse_list = []
        test_r2_list = []
        test_pred_list = []
        test_error_list = []
        fold_number = 0

        kf = KFold(n_splits=int(1 / test_ratio))

        if sort_before_split:
            (
                X_train_val,
                X_test,
                Y_train_val,
                Y_test,
            ) = sort_train_test_split_shuffle(X, Y, test_ratio=test_ratio, seed=1)
        else:
            X_train_val, X_test, Y_train_val, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)
        Y_test = Y_test.astype("float")

        for train_index, test_index in kf.split(X_train_val):
            fold_number += 1
            X_train, X_val = X_train_val[train_index], X_train_val[test_index]
            Y_train, Y_val = (
                Y_train_val[train_index].astype("float"),
                Y_train_val[test_index].astype("float"),
            )

            # Create copy for the model
            model = self.new_instance(self.__class__, **kwargs)

            # Transform the data
            (model.X_train, model.Y_train, model.X_val, model.Y_val, model.X_test, model.Y_test,) = (
                X_train,
                Y_train,
                X_val,
                Y_val,
                X_test,
                Y_test,
            )
            if model.variables.num_cat_var > 0:
                model.X_train = model.variables.categorical_transform(model.X_train).astype("float")
                model.X_val = model.variables.categorical_transform(model.X_val).astype("float")
                model.X_test = model.variables.categorical_transform(model.X_test).astype("float")
            else:
                model.X_train = X_train
                model.X_val = X_val
                model.X_test = X_test

            model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, model.Y_train)
            model.X_val, model.Y_val = model.transform_only_by_predictor_type(model.X_val, model.Y_val)
            (
                model.X_test,
                model.Y_test,
            ) = model.transform_only_by_predictor_type(model.X_test, model.Y_test)

            model.fit_model(self.model_params)

            # Make predictions and calculate model performance
            model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
            model.Y_val_pred, model.Y_val_pred_stddev = model.predict(X_val)
            model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
            model.performance_metrics = pm.all_performance_metrics_train_val_test(
                Y_train,
                model.Y_train_pred,
                Y_val,
                model.Y_val_pred,
                Y_test,
                model.Y_test_pred,
            )
            model.Y_test_error = 1.96 * model.Y_test_pred_stddev

            cv_results[f"Fold {fold_number}"] = {
                "Performance Metrics": model.performance_metrics,
                "Model": model.model,
            }
            test_rmse_list.append(model.performance_metrics["Test RMSE"])
            test_r2_list.append(model.performance_metrics["Test r2"])
            test_pred_list.append(model.Y_test_pred.flatten())
            test_error_list.append(model.Y_test_error.flatten())

        cv_results["Mean Test RMSE"] = np.mean(test_rmse_list)
        cv_results["Mean Test r2"] = np.mean(test_r2_list)
        cv_results["Mean Y Test Parity Data"] = pm.paritydata(Y_test, np.mean(test_pred_list, axis=0))
        cv_results["Mean Y Test Error (CI 95%)"] = np.mean(test_error_list, axis=0)

        logger.info(
            f"Completed {self.name} CV (k = {int(1/test_ratio)}) model checking | Mean Test Loss: {cv_results['Mean Test RMSE']}"
        )

        return cv_results

    def non_cv_train_test(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> float:

        self.model_params = model_params

        # Split the dataset
        if sort_before_split:
            (
                X_train,
                X_test,
                Y_train,
                Y_test,
            ) = sort_train_test_split_shuffle(X, Y, test_ratio=test_ratio, seed=1)
        else:
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)

        # Create copy for the model
        model = self.new_instance(self.__class__, **kwargs)

        # Transform the data
        model.X_train, model.Y_train, model.X_test, model.Y_test = (
            X_train,
            Y_train,
            X_test,
            Y_test,
        )
        if model.variables.num_cat_var > 0:
            model.X_train = model.variables.categorical_transform(model.X_train).astype("float")
            model.X_test = model.variables.categorical_transform(model.X_test).astype("float")

        model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, Y=model.Y_train)
        model.X_test, model.Y_test = model.transform_only_by_predictor_type(model.X_test, Y=model.Y_test)

        model.fit_model(self.model_params)

        # Make predictions and calculate model performance
        model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
        model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
        model.performance_metrics = pm.all_performance_metrics_train_val(
            Y_train, model.Y_train_pred, Y_test, model.Y_test_pred
        )

        return model.performance_metrics["Test RMSE"]

    def non_cv_train_val_test(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> float:
        self.model_params = model_params

        # Split the dataset
        if sort_before_split:
            (
                X_train,
                X_val,
                X_test,
                Y_train,
                Y_val,
                Y_test,
            ) = sort_train_val_test_split_shuffle(X, Y, test_ratio=test_ratio, seed=1)
        else:
            X_train_val, X_test, Y_train_val, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)
            X_train, X_val, Y_train, Y_val = train_test_split(
                X_train_val, Y_train_val, test_size=test_ratio, random_state=1
            )

        # Create copy for the model
        model = self.new_instance(self.__class__, **kwargs)

        # Transform the data
        if model.variables.num_cat_var > 0:
            model.X_train = model.variables.categorical_transform(X_train).astype("float")
            model.X_val = model.variables.categorical_transform(X_val).astype("float")
            model.X_test = model.variables.categorical_transform(X_test).astype("float")
        else:
            model.X_train = X_train
            model.X_val = X_val
            model.X_test = X_test

        model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, Y=Y_train)
        model.X_val, model.Y_val = model.transform_only_by_predictor_type(model.X_val, Y=Y_val)
        model.X_test, model.Y_test = model.transform_only_by_predictor_type(model.X_test, Y=Y_test)

        model.fit_model(self.model_params)

        # Make predictions and calculate model performance
        model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
        model.Y_val_pred, model.Y_val_pred_stddev = model.predict(X_val)
        model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
        model.performance_metrics = pm.all_performance_metrics_train_val_test(
            Y_train, model.Y_train_pred, Y_val, model.Y_val_pred, Y_test, model.Y_test_pred
        )

        return model.performance_metrics["Test RMSE"]

    def y_scrambling_cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        plot_parity=True,
        inc_error_bars: bool = False,
        **kwargs,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Compares the model fitting and accuracy of test data using cross validation for the original data set and a Y-scrambled data set

        Parameters
        ----------
        predictor_type : str or list of str type for the type of model to use. Default is None. When None, all model types in NEMO will be tested
            "gp" : Gaussian process models
            "nn_concrete" : Neural networks with automatic tuning of the dropout probability
            "nn_ensemble" : Deep Ensembles of neural networks
            "nn_bayesian" : Bayesian neural network from learning weight distributions
            "xgb" : XGBoost for probabilistic prediction
            "ngb" : NGBoost algorithm with natural gradient boosting for probabilistic prediction
        model_params : dict type containing the keyword hyperparameter arguments to use for model fitting
        plot_parity : bool type for generating the parity plot for the model fitting performance
        inc_error_bars : bool type for if error bars corresponding to a 95% confidence interval should drawn in the parity plot

        Returns
        -------
        cv_results : dict type containing the performance metrics from the fitted models using the original data set, with emphasis on the test data Results
        cv_results_y_scrambling : dict type containing the performance metrics from the fitted models using the Y-scrambled data set, with emphasis on the test data Results

        """

        dirname_y_scrambling = os.path.join(os.getcwd(), "ML Models", f"{self.name}", "Y-Scrambling")
        if not os.path.exists(dirname_y_scrambling):
            os.makedirs(dirname_y_scrambling)

        cv_results = self.cv_train_val_test(X, Y, model_params, test_ratio=test_ratio, **kwargs)

        np.random.seed(0)
        np.random.shuffle(Y)

        cv_results_y_scrambling = self.cv_train_val_test(X, Y, model_params, test_ratio=test_ratio, **kwargs)

        if plot_parity:
            # Produces a 2D scatter plot showing the parity plot data points, and the x = y line as a line plot
            original_paritydata = cv_results["Mean Y Test Parity Data"]
            y_scrambling_paritydata = cv_results_y_scrambling["Mean Y Test Parity Data"]

            original_error = cv_results["Mean Y Test Error (CI 95%)"]
            y_scrambling_error = cv_results_y_scrambling["Mean Y Test Error (CI 95%)"]

            original_rmse = cv_results["Mean Test RMSE"]
            y_scrambling_rmse = cv_results_y_scrambling["Mean Test RMSE"]
            original_r2 = cv_results["Mean Test r2"]
            y_scrambling_r2 = cv_results_y_scrambling["Mean Test r2"]

            scatter_parity_data = [original_paritydata, y_scrambling_paritydata]
            error = [original_error, y_scrambling_error]
            max_parity = np.vstack([original_paritydata, y_scrambling_paritydata]).max()
            min_parity = np.vstack([original_paritydata, y_scrambling_paritydata]).min()
            # Array for the x = y line in the parity plot
            x_equals_y = [
                [min_parity, min_parity],
                [max_parity, max_parity],
            ]
            scatter_legend = (
                f"Original ({original_paritydata.shape[0]} Test Data Points)",
                f"Y-Scrambling ({y_scrambling_paritydata.shape[0]} Test Data Points)",
            )
            plot_title = f"Original and Y-Scrambling Test Data Parity Plot\nOriginal Test RMSE = {round(original_rmse.astype('float'), 2)}, Original Test r2 = {round(original_r2, 2)}\nY-Scrambling Test RMSE = {round(y_scrambling_rmse.astype('float'), 2)}, Y-Scrambling Test r2 = {round(y_scrambling_r2, 2)}"
            output_file = os.path.join(
                dirname_y_scrambling,
                f"Y-Scrambling Test Data Parity Plot, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
            )
            if inc_error_bars:
                plotter.plot(
                    plot_dim="2D",
                    scatter_data=scatter_parity_data,
                    error=error,
                    line_data=x_equals_y,
                    scatter_legend=scatter_legend,
                    line_legend="x = y",
                    xlabel=f"Actual",
                    ylabel=f"Predicted",
                    plottitle=plot_title,
                    output_file=output_file,
                )
            else:
                plotter.plot(
                    plot_dim="2D",
                    scatter_data=scatter_parity_data,
                    # error=error,
                    line_data=x_equals_y,
                    scatter_legend=scatter_legend,
                    line_legend="x = y",
                    xlabel=f"Actual",
                    ylabel=f"Predicted",
                    plottitle=plot_title,
                    output_file=output_file,
                )
            plt.close()

        logger.info(
            f"Completed Y-scrambling CV tests | Mean Test Loss: {cv_results['Mean Test RMSE']} | Y-scrambling Mean Test Loss: {cv_results_y_scrambling['Mean Test RMSE']}"
        )

        return cv_results, cv_results_y_scrambling

    def permutation_feature_importance(
        self, X: np.ndarray, Y: np.ndarray, repeats: int = 50
    ) -> Tuple[pd.Series, pd.Series]:
        logger.info(f"Performing permutation feature importance calculation for {self.name} model")

        Y_pred_base, _ = self.predict(X)
        mse_score_base = mean_squared_error(Y, Y_pred_base)

        results = []
        for i in range(X.shape[1]):
            temp_i_store = copy.copy(X[:, i])

            mse_score_i_shuffled_list = []
            for repeat in range(repeats):
                np.random.shuffle(X[:, i])
                Y_pred_i_shuffled, _ = self.predict(X)
                mse_score_i_shuffled = mean_squared_error(Y, Y_pred_i_shuffled)
                mse_score_i_shuffled_list.append(mse_score_i_shuffled)
                if repeat % 10 == 0:
                    print(
                        f"Variable {i + 1}, Repeat {repeat + 1}, Permutation MSE: {mse_score_i_shuffled}, Difference to Base MSE: {mse_score_i_shuffled - mse_score_base}"
                    )
            X[:, i] = copy.copy(temp_i_store)
            results.append(np.array(mse_score_i_shuffled_list))

        results = np.array(results).T
        results_diff = results - mse_score_base
        feature_importance_mean = np.mean(results_diff, axis=0)
        feature_importance_mean = feature_importance_mean / np.sum(feature_importance_mean)
        feature_importance_stddev = np.std(results_diff, axis=0)

        feature_importance_mean = pd.Series(feature_importance_mean, index=self.variables.names)
        feature_importance_stddev = pd.Series(feature_importance_stddev, index=self.variables.names)

        print(f"Permutation feature importance: {np.around(feature_importance_mean, decimals=3)}")

        logger.info(f"Completed permutation feature importance calculation")

        return feature_importance_mean, feature_importance_stddev

    def permutation_feature_importance_continuous(
        self, X: np.ndarray, Y: np.ndarray, repeats: int = 50
    ) -> Tuple[pd.Series, pd.Series]:
        logger.info(f"Performing permutation feature importance calculation for {self.name} model")

        Y_pred_base, _ = self.predict(X)
        mse_score_base = mean_squared_error(Y, Y_pred_base)

        # Convert categorical variables names to descriptors
        if self.variables.num_cat_var > 0:
            X = self.variables.categorical_transform(X)

        # Transform the continuous variables and descriptors
        X = self.transform_only_by_predictor_type(X)

        results = []
        for i in range(X.shape[1]):
            temp_i_store = copy.copy(X[:, i])

            mse_score_i_shuffled_list = []
            for repeat in range(repeats):
                np.random.shuffle(X[:, i])

                Y_pred_i_shuffled, _ = self.predict(X, X_transform=False)

                mse_score_i_shuffled = mean_squared_error(Y, Y_pred_i_shuffled.flatten())
                mse_score_i_shuffled_list.append(mse_score_i_shuffled)
                if repeat % 10 == 0:
                    print(
                        f"Variable {i + 1}, Repeat {repeat + 1}, Permutation MSE: {mse_score_i_shuffled}, Difference to Base MSE: {mse_score_i_shuffled - mse_score_base}"
                    )
            X[:, i] = copy.copy(temp_i_store)
            results.append(np.array(mse_score_i_shuffled_list))

        results = np.array(results).T
        results_diff = results - mse_score_base
        feature_importance_mean = np.mean(results_diff, axis=0)
        feature_importance_mean = feature_importance_mean / np.sum(feature_importance_mean)
        feature_importance_stddev = np.std(results_diff, axis=0)

        feature_importance_mean = pd.Series(feature_importance_mean, index=self.variables.continuous_var_names)
        feature_importance_stddev = pd.Series(feature_importance_stddev, index=self.variables.continuous_var_names)

        print(f"Permutation feature importance:\n{np.around(feature_importance_mean, decimals=3)}")

        logger.info(f"Completed permutation feature importance calculation")

        return feature_importance_mean, feature_importance_stddev

    def partial_dependence_plot(self, X: np.ndarray) -> Dict[str, pd.DataFrame]:
        logger.info(f"Creating partial dependence plots for {self.name} model")
        path = os.path.join(os.getcwd(), "ML Models", f"{self.name}", "Partial Dependence Plots")
        if not os.path.exists(path):
            os.makedirs(path)

        if self.variables.num_cat_var > 0:
            X = self.variables.categorical_transform(X)

        X = self.transform_only_by_predictor_type(X)

        X_copy = copy.copy(X)

        pdp_dict = {}
        for index, col in enumerate(X.T):
            Y_pred_pdp = []
            for value in col:
                X_copy[:, index] = value

                Y_pred, _ = self.predict(X_copy, X_transform=False)
                Y_pred_pdp.append([value, Y_pred.mean()])

            Y_pred_pdp_np = np.array(Y_pred_pdp)
            pdp_dict[self.variables.continuous_var_names[index]] = pd.DataFrame(
                Y_pred_pdp_np,
                columns=[
                    f"{self.variables.continuous_var_names[index]}",
                    f"{self.objective.name}",
                ],
            )
            X_copy[:, index] = col

            plotter.plot(
                plot_dim="2D",
                scatter_data=Y_pred_pdp_np,
                scatter_legend=f"Number of Grid Points = {Y_pred_pdp_np.shape[0]}",
                xlabel=f"{self.variables.continuous_var_names[index]}",
                ylabel=f"{self.objective.name} ({self.objective.units})",
                plottitle=f"Partial Dependence Plot for {self.objective.name} against {self.variables.continuous_var_names[index]}",
                output_file=os.path.join(
                    path,
                    rf"Partial Dependence Plot for {self.objective.name} against {self.variables.continuous_var_names[index]}, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
                ),
            )
            plt.close("all")

        logger.info(f"Completed partial dependence plot calculations")

        return pdp_dict

    def transform_by_predictor_type(
        self, X: np.ndarray, Y: Optional[np.ndarray] = None
    ) -> np.ndarray | Tuple[np.ndarray, np.ndarray]:
        X = self.variables.transform(X, self.default_X_transform_type)

        if Y is not None:
            if self.objective.transformation_type is None:
                self.objective.transformation_type = self.default_Y_transform_type
            Y = self.objective.transform(Y)
            return X.astype("float"), Y.astype("float")
        else:
            return X.astype("float")

    def transform_only_by_predictor_type(
        self, X: np.ndarray, Y: Optional[np.ndarray] = None
    ) -> np.ndarray | Tuple[np.ndarray, np.ndarray]:
        X = self.variables.transform_only(X)

        if Y is not None:
            Y = self.objective.transform_only(Y)
            return X.astype("float"), Y.astype("float")
        else:
            return X.astype("float")
