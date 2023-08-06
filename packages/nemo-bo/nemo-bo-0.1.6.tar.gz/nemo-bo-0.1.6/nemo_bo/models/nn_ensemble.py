from __future__ import annotations

import math
import os
from datetime import datetime
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll.base import scope
from keras import backend as K
from keras import callbacks
from keras.layers import Dense, Dropout, Input
from keras.models import Model
from keras.optimizers import Optimizer
from sklearn.model_selection import train_test_split
from tensorflow import keras

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
from nemo_bo.models.base.base_model import Base_Model
from nemo_bo.models.base.nn_save_checkpoint import SaveModelCheckPoint
from nemo_bo.utils.data_proc import sort_train_test_split_shuffle

if TYPE_CHECKING:
    from nemo_bo.opt.objectives import RegressionObjective
    from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


tfpl = tfp.layers
tfd = tfp.distributions

gpus = tf.config.list_physical_devices("GPU")
if gpus:
    try:
        # Memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.list_logical_devices("GPU")
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)


class NNEnsembleModel(Base_Model):
    """
    Class to instantiate for fitting neural network models using TensorFlow
    """

    def __init__(
        self,
        variables: VariablesList,
        objective: RegressionObjective,
        always_hyperparam_opt: bool = False,
        es_patience: int = 300,
        **kwargs,
    ):  # normally 300
        """

        Parameters
        ----------
        X : 2D numpy.ndarray type of un_transformed input variables
        Y : 1D numpy.ndarray type of un_transformed target objective values
        test_ratio : float type of the test:train size ratio desired (e.g. 0.2 for 20% test size)
        data_split_mode : str type for selecting the type of data pre-processing to perform on the X values with respect to splitting for train, validation, and test sets where applicable
            "train_val" : Split into train and validation sets typically used for fitting models with optimised hyperparameters
            "train_val_test" : Split into train, validation, and test sets that can be used for hyperparameter opt and model evaluation
            "cv" : Split into train, validation, and test sets for use in cross-validation for hyperparameter opt and model evaluation
        num_epochs : int type for the maximum number of epochs to allow for training. Default: 4000
        act_func : str type for the activation function to use. Default: 'relu'
        optimizer : Keras optimiser subclasses that implement the desired algorithm, such as Adam, RMSprop, etc. Default: keras.optimizers.Adam
        seed : int type for a randomisation seed for data shuffling during pre-processing

        """
        super().__init__(variables, objective, always_hyperparam_opt)
        self.default_X_transform_type = "standardisation"
        self.default_Y_transform_type = "standardisation"
        self.include_validation = True
        self.name = "nn_ensemble"

        self.earlystopping = callbacks.EarlyStopping(
            monitor="val_loss",
            min_delta=0.001,
            patience=es_patience,
            verbose=0,
            mode="min",
        )

        self.dirname_checkpoint = os.path.join(os.getcwd(), "ML Models", "nn_ensemble", "Checkpoints")
        if not os.path.exists(self.dirname_checkpoint):
            os.makedirs(self.dirname_checkpoint)

    @staticmethod
    def negloglik(y_data, rv_y):
        """
        Function to calculate the value of the negative loglikelihood function
        """
        return -rv_y.log_prob(y_data)

    # function for creating a fully connected neural network of any architecture
    # the number of neurons in each layer is defined by layers_shape
    # the droupout_proba indicates if dropout layers should be added
    def structure(
        self,
        X_train: np.ndarray,
        learning_rate: float,
        hidden_units: int,
        hidden_layers: int,
        dropout_proba: float,
        act_func: str,
        optimizer: Optimizer,
    ) -> Model:
        """
        Function that defines the structure of the input, hidden layers, and output required for an ensemble of neural network models

        Parameters
        ----------
        learning_rate : float type for assigning the learning rate for the optimiser
        hidden_units : int type for the number of hidden units within every hidden layer. Currently, all hidden layers will have this number of hidden units
        hidden_layers : int type for the number of hidden layers in the neural network
        dropout_proba : float type for the dropout probability to be applied to the hidden layers

        Returns
        -------
        model : The neural network model to fit that will be part of an ensemble

        """
        K.clear_session()
        tf.random.set_seed(1)
        tf.random.uniform([1], seed=1)
        input_data = Input((X_train.shape[1],))
        x = input_data
        for _ in range(hidden_layers):
            x = Dense(hidden_units, activation=act_func)(x)
            if dropout_proba > 0:
                x = Dropout(dropout_proba)(x)

        x = Dense(2)(x)
        x = tfpl.DistributionLambda(lambda t: tfd.Normal(loc=t[..., :1], scale=1e-3 + tf.math.softplus(t[..., 1:])))(x)
        model = Model(input_data, x)
        model.summary()

        model.compile(
            optimizer=optimizer(learning_rate=learning_rate),
            loss=self.negloglik,
            metrics=["mse"],
        )

        return model

    def fit(
        self, X: np.ndarray, Y: np.ndarray, test_ratio: Optional[float] = None, sort_before_split: bool = None, **params
    ) -> None:
        """
        Function for fitting the model

        Parameters
        ----------
        learning_rate : float type for assigning the learning rate for the optimiser. Default: 0.001
        hidden_units : int type for the number of hidden units within every hidden layer. Currently, all hidden layers will have this number of hidden units. Default: 18
        hidden_layers : int type for the number of hidden layers in the neural network. Default: 2
        batch_size : int type for the batch size to use for the data set used. Default: 32
        dropout_proba : float type for the dropout probability to be applied to the hidden layers. Default: 0.001
        ensemble_size: int type for the number of neural networks to fit and be part of the ensemble. Default: 5
        plot_parity : bool type for generating the parity plot for the model fitting performance

        """
        if sort_before_split:
            (
                X_train,
                X_val,
                Y_train,
                Y_val,
            ) = sort_train_test_split_shuffle(X, Y, test_ratio=test_ratio, seed=1)
        else:
            X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=test_ratio, random_state=1)

        Y_train = Y_train.astype("float")
        Y_val = Y_val.astype("float")

        self.X_train, self.X_val, self.Y_train, self.Y_val = (
            X_train,
            X_val,
            Y_train,
            Y_val,
        )
        if self.variables.num_cat_var > 0:
            self.X_train = self.variables.categorical_transform(self.X_train).astype("float")
            self.X_val = self.variables.categorical_transform(self.X_val).astype("float")

        self.X_train, self.Y_train = self.transform_by_predictor_type(self.X_train, Y=self.Y_train)
        self.X_val, self.Y_val = self.transform_only_by_predictor_type(self.X_val, self.Y_val)

        self.fit_model(params)

        self.Y_train_pred, self.Y_train_pred_stddev = self.predict(X_train)
        self.Y_val_pred, self.Y_val_pred_stddev = self.predict(X_val)
        self.performance_metrics = pm.all_performance_metrics_train_val(
            Y_train, self.Y_train_pred, Y_val, self.Y_val_pred
        )

        self.Y_train_error = 1.96 * self.Y_train_pred_stddev
        self.Y_val_error = 1.96 * self.Y_val_pred_stddev

    def fit_model(self, params: Dict[str, Any]) -> None:
        hidden_units = int(params.get("hidden_units", self.X_train.shape[1] + 1))
        hidden_layers = int(params.get("hidden_layers", 2))
        batch_size = int(params.get("batch_size", 32))
        learning_rate = params.get("learning_rate", 0.001)
        dropout_proba = params.get("dropout_proba", 0.001)
        ensemble_size = int(params.get("ensemble_size", 5))
        max_epochs = int(params.get("max_epochs", 4000))
        act_func = params.get("act_func", "relu")
        optimizer = params.get("optimizer", keras.optimizers.Adam)

        self.filepath = os.path.join(
            self.dirname_checkpoint,
            f"Checkpoint, Ensemble, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.h5",
        )

        self.ensemble_model_list = []
        for _ in range(ensemble_size):
            self.model = self.structure(
                self.X_train,
                learning_rate,
                hidden_units,
                hidden_layers,
                dropout_proba,
                act_func,
                optimizer,
            )
            self.savemodelcheckpoint = SaveModelCheckPoint(self.model, self.filepath)  # A Simon Original
            self.history = self.model.fit(
                self.X_train,
                self.Y_train,
                validation_data=(self.X_val, self.Y_val),
                epochs=max_epochs,
                verbose=2,
                batch_size=batch_size,
                callbacks=[
                    callbacks.LambdaCallback(on_epoch_end=self.savemodelcheckpoint.save_weights),
                    self.earlystopping,
                ],
            )

            self.model = self.structure(
                self.X_train,
                learning_rate,
                hidden_units,
                hidden_layers,
                dropout_proba,
                act_func,
                optimizer,
            )
            self.model.load_weights(self.filepath)
            self.ensemble_model_list.append(self.model)

    def predict(self, X: np.ndarray, X_transform: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        # The functions below require the data to be a 2D array
        if X.ndim == 1:
            X = X.reshape(1, -1)

        if X_transform:
            if self.variables.num_cat_var > 0:
                X = self.variables.categorical_transform(X).astype("float")
            X = self.transform_only_by_predictor_type(X)

        observed_Y_pred = [ensemble_model(X) for ensemble_model in self.ensemble_model_list]
        Y_pred = np.array([prediction.loc.numpy() for prediction in observed_Y_pred])
        Y_pred_stddev = np.array([prediction.scale.numpy() for prediction in observed_Y_pred])

        # Code adapted from:
        #     1. João Caldeira, Brian Nord, Deeply Uncertain: Comparing Methods of Uncertainty Quantification in Deep Learning Algorithms, arXiv:2004.10710, https://github.com/deepskies/DeeplyUncertain-Public,
        #     2. Yarin Gal, Jiri Hron, Alex Kendall, Concrete Dropout, arXiv:1705.07832, https://github.com/yaringal/ConcreteDropout
        Y_val_epistemic_unc = np.std(np.array(Y_pred), axis=0)  # Equation 4 from paper
        Y_val_aleatoric_unc = np.sqrt(np.mean(np.array(Y_pred_stddev) * np.array(Y_pred_stddev), axis=0))
        Y_val_total_unc = np.sqrt(Y_val_aleatoric_unc**2 + Y_val_epistemic_unc**2)

        Y_pred = np.mean(Y_pred, axis=0)
        Y_pred_upper = Y_pred + (1.96 * Y_val_total_unc)

        Y_pred = self.objective.inverse_transform(Y_pred)
        Y_pred_upper = self.objective.inverse_transform(Y_pred_upper)
        Y_pred_stddev = (np.subtract(Y_pred_upper, Y_pred)) / 1.96

        return Y_pred.flatten(), Y_pred_stddev.flatten()

    @staticmethod
    def default_params(X: np.ndarray):
        return {
            "learning_rate": hp.uniform("learning_rate", 0.001, 0.01),
            "hidden_units": scope.int(hp.quniform("hidden_units", math.ceil(X.shape[1] / 2), (X.shape[1] + 1), 1)),
            "hidden_layers": scope.int(hp.quniform("hidden_layers", 1, 2, 1)),
            "batch_size": scope.int(hp.quniform("batch_size", math.ceil(X.shape[0] / 10), X.shape[0], 1)),
            "dropout_proba": hp.uniform("dropout_proba", 0.001, 0.05),
        }

    # def cv(
    #     self,
    #     X: np.ndarray,
    #     Y: np.ndarray,
    #     model_params: Dict[str, Any],
    #     test_ratio: float = 0.2,
    #     sort_before_split: Optional[bool] = True,
    #     **kwargs,
    # ) -> Dict[str, Any]:
    #     return self.cv_train_val_test(
    #         X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs
    #     )

    def hyperparam_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float,
        sort_before_split: bool = True,
        predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None,
        **kwargs,
    ) -> Tuple[float, Dict[str, Any]]:

        if predictor_params_dict is None:
            predictor_params_dict = self.default_params(X)
        else:
            predictor_params_dict = predictor_params_dict[self.name]

        max_evals = kwargs.get("max_evals", 1)
        # max_evals = kwargs.get("max_evals", 15)

        def func(X: np.ndarray, Y: np.ndarray, model_params: Dict[str, Any]) -> Dict[str, Any]:
            loss = self.non_cv_train_val_test(
                X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs
            )

            return {
                "loss": loss,
                "status": STATUS_OK,
            }

        trials = Trials()
        model_params = fmin(
            fn=partial(func, X, Y),
            space=predictor_params_dict,
            algo=tpe.suggest,
            max_evals=max_evals,
            trials=trials,
        )

        model = self.new_instance(self.__class__, **kwargs)
        model.fit(X, Y, test_ratio=test_ratio, **self.model_params, **kwargs)

        logger.info(f"Completed hyperparameter opt")
        return model, model_params
