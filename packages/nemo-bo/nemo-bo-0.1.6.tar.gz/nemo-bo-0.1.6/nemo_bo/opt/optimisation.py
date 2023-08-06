import ast
import os
import pickle
from attrs import define, field
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.plotter as plotter
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.acquisition_functions.expected_improvement.expected_improvement import ExpectedImprovement
from nemo_bo.opt.benchmark import Benchmark
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList, RegressionObjective
from nemo_bo.opt.samplers import LatinHyperCubeSampling, PoolBased, SampleGenerator
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class Optimisation:
    variables: VariablesList
    objectives: ObjectivesList
    acquisition_func: AcquisitionFunction
    sampler: Optional[Union[SampleGenerator, PoolBased]] = None
    constraints: Optional[ConstraintsList] = None
    benchmark_func: Optional[Benchmark] = None
    optimisation_dict: Dict[str, Any] = field(init=False)
    X_columns: List[str] = field(init=False)
    Y_columns: List[str] = field(init=False)
    X: np.ndarray = field(init=False)
    Y: np.ndarray = field(init=False)
    optimisation_only: pd.DataFrame = field(init=False)
    selected_X: np.ndarray = field(init=False)
    selected_Y: np.ndarray = field(init=False)

    def __attrs_post_init__(self):
        if isinstance(self.acquisition_func, ExpectedImprovement) and self.sampler is None:
            self.sampler = LatinHyperCubeSampling()

        self.optimisation_dict = {}

        self.X_columns = []
        for name, units in zip(self.variables.names, self.variables.units):
            if units == "":
                self.X_columns.append(name)
            else:
                self.X_columns.append(f"{name} ({units})")

        self.Y_columns = []
        for name, units in zip(self.objectives.names, self.objectives.units):
            if units == "":
                self.Y_columns.append(name)
            else:
                self.Y_columns.append(f"{name} ({units})")

    def run(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        number_of_iterations: int = 200,
        test_ratio: float = 0.2,
        number_opt_iterations_completed: int = 0,
        model_run_counter: int = 0,
        model_run_counter_threshold: int = 5,
        plot_pareto_hypervolume: bool = False,
        **kwargs,
    ) -> Dict[str, Dict[str, Any]]:
        self.X = X
        self.Y = Y

        for iteration in range(number_of_iterations):
            if model_run_counter % model_run_counter_threshold == 0:
                model_search_bool = True
                print("Will perform automated model and hyperparameter selection")
            else:
                model_search_bool = False
                print("Depending on predictor type, will perform model fitting with stored hyperparameters")

            if plot_pareto_hypervolume:
                # Plot pareto plot without predicted experiment values
                self.plot_scatter2d_opt(
                    Y=self.Y,
                    number_opt_iterations=number_opt_iterations_completed,
                    inc_predicted=False,
                )

                # Plot hypervolume plot without predicted experiment values
                self.plot_hypervolume(
                    Y=self.Y,
                    number_opt_iterations=number_opt_iterations_completed,
                    inc_predicted=False,
                )

            self.selected_X, self.selected_Y = self.find_candidates(
                self.X,
                self.Y,
                model_search_bool=model_search_bool,
                test_ratio=test_ratio,
                **kwargs,
            )

            suggested_XY = pd.DataFrame(
                np.hstack((self.selected_X, self.selected_Y)),
                columns=self.X_columns + self.Y_columns,
            )
            with pd.option_context("display.max_rows", None, "display.max_columns", None):
                print(suggested_XY)

            if not isinstance(self.sampler, PoolBased) and self.benchmark_func is None:
                if not os.path.exists(os.path.join(os.getcwd(), "Results")):
                    os.makedirs(os.path.join(os.getcwd(), "Results"))
                suggested_XY.to_excel(
                    os.path.join(
                        os.getcwd(),
                        "Results",
                        f"Iteration {iteration + 1} suggested candidates {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.xlsx",
                    )
                )
                while True:
                    try:
                        actual_result = ast.literal_eval(
                            input(
                                f"Variables for the current opt iteration have been suggested (see print or 'Iteration {iteration + 1} suggested candidates.xlsx')\nPlease input the actual results in a python list:\n"
                            )
                        )
                        assert isinstance(actual_result, list)

                        self.selected_Y = (
                            np.array(actual_result)
                            if self.acquisition_func.num_candidates > 1
                            else np.array(actual_result).reshape(1, -1)
                        )

                        assert (
                            self.selected_Y.shape[0] == self.acquisition_func.num_candidates
                            and self.selected_Y.shape[1] == self.objectives.n_obj
                            and np.issubdtype(self.selected_Y.dtype, np.number)
                        )

                        break
                    except AssertionError:
                        print(
                            "\nAssertionError: Please ensure that you have inputted the actual numerical results in a python list with the correct dimensions for the number of candidates (x) and number of objectives (y)\n"
                        )
                    except IndexError:
                        print(
                            "\nIndexError: Please ensure that you have inputted the actual numerical results in a python list with the correct dimensions for the number of candidates (x) and number of objectives (y)\n"
                        )
                    except ValueError:
                        print(
                            "\nIndexError: Please ensure that you have inputted the actual numerical results in a python list with the correct dimensions for the number of candidates (x) and number of objectives (y)\n"
                        )
                    except SyntaxError:
                        print(
                            "\nIndexError: Please ensure that you have inputted the actual numerical results in a python list with the correct dimensions for the number of candidates (x) and number of objectives (y)\n"
                        )

            self.X = np.vstack((self.X, self.selected_X))
            self.Y = np.vstack((self.Y, self.selected_Y))

            self.save(iteration, model_search_bool, model_run_counter)

            if self.acquisition_func.reset or model_search_bool:
                model_run_counter = 1
            else:
                model_run_counter += 1

            number_opt_iterations_completed += 1

        return self.optimisation_dict

    def find_candidates(self, X: np.ndarray, Y: np.ndarray, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        if any(isinstance(obj, RegressionObjective) for obj in self.objectives.objectives):

            # Fit the ML regression models
            self.objectives.fit(X, Y, self.variables, **kwargs)

        # Use the acquisition function
        selected_X, selected_Y = self.acquisition_func.generate_candidates(
            Y, self.variables, self.objectives, self.sampler, self.constraints, **kwargs
        )

        if isinstance(self.sampler, PoolBased):
            selected_Y = self.sampler.Y_and_update_pool(self.sampler.index)

        else:
            if self.benchmark_func is not None:
                if self.benchmark_func.fitted:
                    selected_Y, _ = self.benchmark_func.evaluate(self.selected_X)
                else:
                    raise AttributeError("Please firstly fit the benchmark function(s) and check its quality")

        return selected_X, selected_Y

    def save(self, iteration: int, model_search_bool: bool, model_run_counter: int) -> None:
        # Save excel for current iteration data
        if not os.path.exists(os.path.join(os.getcwd(), "Results")):
            os.makedirs(os.path.join(os.getcwd(), "Results"))

        model_info_list = [model_search_bool, model_run_counter]
        model_info_columns = [
            "Model and Hyperparameter Optimisation",
            "Model Run Counter",
        ]
        for obj in self.objectives.objectives:
            if isinstance(obj, RegressionObjective):
                if obj.obj_function.include_validation:
                    model_info_list.append(obj.obj_function.performance_metrics["Train RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["Train r2"])
                    model_info_list.append(obj.obj_function.performance_metrics["Validation RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["Validation r2"])
                    model_info_columns.append(f"{obj.name} Model Train RMSE")
                    model_info_columns.append(f"{obj.name} Model Train r2")
                    model_info_columns.append(f"{obj.name} Model Validation RMSE")
                    model_info_columns.append(f"{obj.name} Model Validation r2")
                else:
                    model_info_list.append(obj.obj_function.performance_metrics["RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["r2"])
                    model_info_columns.append(f"{obj.name} Model Train RMSE")
                    model_info_columns.append(f"{obj.name} Model Train r2")
                model_info_list.append(obj.obj_function.name)
                model_info_list.append(obj.model_params)
                model_info_columns.append(f"{obj.name} Model Type")
                model_info_columns.append(f"{obj.name} Model Hyperparameters")

        model_info_list.append(datetime.now().strftime("%d-%m-%Y, %H-%M-%S"))
        model_info_columns.append("Date and Time")
        model_info = np.array([model_info_list] * self.acquisition_func.num_candidates)

        optimisation_results = pd.DataFrame(np.hstack((self.X, self.Y)), columns=self.X_columns + self.Y_columns)
        if iteration == 0:
            self.optimisation_only = pd.DataFrame(
                np.hstack((self.selected_X, self.selected_Y, model_info)),
                columns=self.X_columns + self.Y_columns + model_info_columns,
            )
        else:
            self.optimisation_only = pd.concat(
                (
                    self.optimisation_only,
                    pd.DataFrame(
                        np.hstack((self.selected_X, self.selected_Y, model_info)),
                        columns=self.X_columns + self.Y_columns + model_info_columns,
                    ),
                ),
                axis=0,
                ignore_index=True,
            )

        with pd.ExcelWriter(
            os.path.join(
                os.getcwd(),
                "Results",
                f'Optimisation Results (after {iteration + 1} iteration(s)) {datetime.now().strftime("%d-%m-%Y, %H-%M-%S")}.xlsx',
            )
        ) as writer:
            optimisation_results.to_excel(writer, sheet_name="Training + Opt")
            self.optimisation_only.to_excel(writer, sheet_name="Only Opt")
            for obj in self.objectives.objectives:
                if isinstance(obj, RegressionObjective):
                    if obj.obj_function.include_validation:
                        obj.obj_function.performance_metrics["Train Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Train Parity Data"
                        )
                        obj.obj_function.performance_metrics["Validation Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Validation Parity Data"
                        )
                    else:
                        obj.obj_function.performance_metrics["Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Train Parity Data"
                        )

        # Saving all model parameters, predictor type, etc, in dictionaries per iteration as a pickle file
        self.optimisation_dict[f"Iteration {iteration + 1}"] = {}
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Date and Time"] = datetime.now().strftime(
            "%d-%m-%Y, %H-%M-%S"
        )
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Training + Optimisation Table"] = optimisation_results
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Optimisation Table"] = self.optimisation_only
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Optimisation Selected X"] = self.selected_X
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Optimisation Selected Y"] = self.selected_Y
        self.optimisation_dict[f"Iteration {iteration + 1}"][
            "Model and Hyperparameter Optimisation"
        ] = model_search_bool
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Model Run Counter"] = model_run_counter
        for obj in self.objectives.objectives:
            if isinstance(obj, RegressionObjective):
                self.optimisation_dict[f"Iteration {iteration + 1}"][f"{obj.name} Model Type"] = obj.obj_function.name
                self.optimisation_dict[f"Iteration {iteration + 1}"][
                    f"{obj.name} Model Hyperparameters"
                ] = obj.model_params
                self.optimisation_dict[f"Iteration {iteration + 1}"][
                    f"{obj.name} Model Performance Metrics"
                ] = obj.obj_function.performance_metrics

        with open(
            os.path.join(
                os.getcwd(),
                "Results",
                f"Optimisation Results (after {iteration + 1} iteration(s)) {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.pickle",
            ),
            "wb",
        ) as handle:
            pickle.dump(self.optimisation_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def plot_scatter2d_opt(self, Y: np.ndarray, number_opt_iterations: int, inc_predicted: bool = False) -> None:

        sign_adjusted_Y = self.acquisition_func.Y_norm_minmax_transform(
            Y, self.objectives.bounds, self.objectives.max_bool_dict
        )

        # Calculates pareto front
        Y_to_expnum = torch.tensor(np.array(sign_adjusted_Y), dtype=torch.double)
        pareto_mask_to_expnum = is_non_dominated(Y_to_expnum)
        pareto_front = Y[pareto_mask_to_expnum]

        # To-do: Currently hard coded to sort for cost which can never be equal to 0
        cost_check = 0
        for obj_index, obj_name in enumerate(self.objectives.names):
            if "Cost" in obj_name:
                pareto_front_sorted = pareto_front[pareto_front[:, obj_index].argsort()]
                cost_check = 1
                break
        if cost_check == 0:
            pareto_front_sorted = pareto_front[pareto_front[:, 0].argsort()]

        if inc_predicted:
            train_experiments = Y[
                : (
                    Y.shape[0]
                    - (number_opt_iterations * self.acquisition_func.num_candidates)
                    - self.acquisition_func.num_candidates
                ),
                :,
            ]
            opt_experiments = Y[
                (
                    Y.shape[0]
                    - (number_opt_iterations * self.acquisition_func.num_candidates)
                    - self.acquisition_func.num_candidates
                ) :,
                :,
            ]
            opt_experiments = opt_experiments[: -self.acquisition_func.num_candidates, :]

            pred_experiments = Y[-self.acquisition_func.num_candidates :, :]
            scatter_data = [train_experiments, opt_experiments, pred_experiments]
            scatter_legend = [
                f"Training ({train_experiments.shape[0]} Experiments)",
                f"Optimisation ({opt_experiments.shape[0]} Experiments)",
                f"Predicted ({pred_experiments.shape[0]} Experiments)",
            ]

            title = "Pareto Plot (inc predicted experiments)"
            output = os.path.join(
                os.getcwd(),
                f'Pareto Plot (inc predicted experiments) {datetime.now().strftime("%d-%m-%Y, %H-%M-%S")}.png',
            )

        else:
            train_experiments = Y[
                : (Y.shape[0] - (number_opt_iterations * self.acquisition_func.num_candidates)),
                :,
            ]
            opt_experiments = Y[
                (Y.shape[0] - (number_opt_iterations * self.acquisition_func.num_candidates)) :,
                :,
            ]
            scatter_data = [train_experiments, opt_experiments]
            scatter_legend = [
                f"Training ({train_experiments.shape[0]} Experiments)",
                f"Optimisation ({opt_experiments.shape[0]} Experiments)",
            ]

            title = "Pareto Plot.png"
            output = os.path.join(
                os.getcwd(),
                f'Pareto Plot {datetime.now().strftime("%d-%m-%Y, %H-%M-%S")}.png',
            )

        plotter.plot(
            plot_dim="2D",
            scatter_data=scatter_data,
            line_data=pareto_front_sorted,
            scatter_legend=scatter_legend,
            line_legend="Pareto front",
            xlabel=f"{self.objectives.names[0]} {self.objectives.units[0]}",
            ylabel=f"{self.objectives.names[1]} {self.objectives.units[1]}",
            plottitle=f"{title}\n{self.objectives.names[0]} vs. {self.objectives.names[1]}",
            output_file=rf"{output}",
        )
        plt.close()

    def plot_hypervolume(self, Y: np.ndarray, number_opt_iterations: int, inc_predicted: bool = False) -> None:

        ref_point = self.acquisition_func.build_ref_point(self.objectives.max_bool_dict)

        sign_adjusted_Y = self.acquisition_func.Y_norm_minmax_transform(
            Y, self.objectives.bounds, self.objectives.max_bool_dict
        )
        # Recalculates the hypervolume for every additional row in the data
        hv_list = [0]
        for y_index in range(2, Y.shape[0] + 2):
            # Calculates pareto front
            obj_data_to_expnum = sign_adjusted_Y[:y_index, :]
            obj_data_to_expnum_np = np.array(obj_data_to_expnum)
            Y_to_expnum = torch.tensor(obj_data_to_expnum_np, dtype=torch.double)
            pareto_mask_to_expnum = is_non_dominated(Y_to_expnum)
            pareto_front_to_expnum = obj_data_to_expnum_np[pareto_mask_to_expnum]

            hv = Hypervolume(ref_point=torch.tensor(ref_point, dtype=torch.double))

            # Calculates the hypervolume
            hv_list.append(hv.compute(torch.tensor(pareto_front_to_expnum, dtype=torch.double)))

        if not inc_predicted:
            num_train_experiments = Y.shape[0] - (number_opt_iterations * self.acquisition_func.num_candidates)
            train_expt_list = [(x + 1) for x in list(range(num_train_experiments))]
            if number_opt_iterations > 0:
                opt_expt_list = [
                    train_expt_list[-1] + ((x + 1) * self.acquisition_func.num_candidates)
                    for x in list(range(number_opt_iterations))
                ]
                opt_num = opt_expt_list[-1] - num_train_experiments
                all_expt_list = train_expt_list + opt_expt_list
            else:
                opt_num = 0
                all_expt_list = train_expt_list

            title = f"Hypervolume\nNumber of training experiments: {num_train_experiments}\nNumber of opt experiments: {opt_num}"
            output_file = os.path.join(
                os.getcwd(),
                rf"Hypervolume vs. Experiment Number {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.png",
            )

        else:
            num_train_experiments = (
                Y.shape[0]
                - (number_opt_iterations * self.acquisition_func.num_candidates)
                - self.acquisition_func.num_candidates
            )
            train_expt_list = [(x + 1) for x in list(range(num_train_experiments))]
            if number_opt_iterations > 0:
                opt_expt_list = [
                    train_expt_list[-1] + ((x + 1) * self.acquisition_func.num_candidates)
                    for x in list(range(number_opt_iterations))
                ]
                all_expt_list = train_expt_list + opt_expt_list + [Y.shape[0]]
                opt_num = opt_expt_list[-1] - num_train_experiments
            else:
                opt_num = 0
                all_expt_list = train_expt_list
            title = f"Hypervolume (including predicted hypervolume)\nNumber of training experiments: {num_train_experiments}\nNumber of opt experiments: {opt_num}\nNumber of predicted experiments: {self.acquisition_func.num_candidates}"
            output_file = os.path.join(
                os.getcwd(),
                rf"Hypervolume vs. Experiment Number (including predicted hypervolume) {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.png",
            )

        hv_array = np.array([[expt_number, hv_list[expt_number]] for expt_number in all_expt_list])
        plotter.plot(
            plot_dim="2D",
            line_data=hv_array,
            line_legend="Hypervolume",
            xlabel=f"Experiment Number",
            ylabel=f"Normalised Hypervolume",
            plottitle=title,
            output_file=output_file,
        )
        plt.close()
