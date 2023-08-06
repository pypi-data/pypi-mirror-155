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
from keras.layers import Dense, Input, InputSpec, Wrapper, concatenate
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


class ConcreteDropout(Wrapper):
    """
    Code copied from:
    João Caldeira, Brian Nord, Deeply Uncertain: Comparing Methods of Uncertainty Quantification in Deep Learning Algorithms, arXiv:2004.10710, https://github.com/deepskies/DeeplyUncertain-Public,

    This wrapper allows to learn the dropout probability for any given input Dense layer.
    ```python
        # as the first layer in a model
        model = Sequential()
        model.add(ConcreteDropout(Dense(8), input_shape=(16)))
        # now model.output_shape == (None, 8)
        # subsequent layers: no need for input_shape
        model.add(ConcreteDropout(Dense(32)))
        # now model.output_shape == (None, 32)
    ```
    `ConcreteDropout` can be used with arbitrary layers which have 2D
    kernels, not just `Dense`. However, Conv2D layers require different
    weighing of the regulariser (use SpatialConcreteDropout instead).
    # Arguments
        layer: a layer instance.
        weight_regularizer:
            A positive number which satisfies
                $weight_regularizer = l**2 / (\tau * N)$
            with prior lengthscale l, model precision $\tau$ (inverse observation noise),
            and N the number of instances in the dataset.
            Note that kernel_regularizer is not needed.
        dropout_regularizer:
            A positive number which satisfies
                $dropout_regularizer = 2 / (\tau * N)$
            with model precision $\tau$ (inverse observation noise) and N the number of
            instances in the dataset.
            Note the relation between dropout_regularizer and weight_regularizer:
                $weight_regularizer / dropout_regularizer = l**2 / 2$
            with prior lengthscale l. Note also that the factor of two should be
            ignored for cross-entropy loss, and used only for the eculedian loss.
    """

    def __init__(
        self,
        layer,
        weight_regularizer=0,
        dropout_regularizer=1e-5,
        init_min=0.1,
        init_max=0.1,
        is_mc_dropout=True,
        **kwargs,
    ):
        assert "kernel_regularizer" not in kwargs
        super(ConcreteDropout, self).__init__(layer, **kwargs)
        self.weight_regularizer = weight_regularizer
        self.dropout_regularizer = dropout_regularizer
        self.is_mc_dropout = is_mc_dropout
        self.supports_masking = True
        self.p_logit = None
        self.init_min = np.log(init_min) - np.log(1.0 - init_min)
        self.init_max = np.log(init_max) - np.log(1.0 - init_max)

    def build(self, input_shape=None):
        self.input_spec = InputSpec(shape=input_shape)
        if not self.layer.built:
            self.layer.build(input_shape)
            self.layer.built = True
        super(ConcreteDropout, self).build()

        # initialise p
        self.p_logit = self.add_weight(
            name="p_logit",
            shape=(1,),
            initializer=tf.random_uniform_initializer(self.init_min, self.init_max),
            dtype=tf.dtypes.float32,
            trainable=True,
        )

    def compute_output_shape(self, input_shape):
        return self.layer.compute_output_shape(input_shape)

    def concrete_dropout(self, x, p):
        """
        Concrete dropout - used at training time (gradients can be propagated)
        :param x: input
        :return:  approx. dropped out input
        """
        eps = 1e-07
        temp = 0.1

        unif_noise = tf.random.uniform(shape=tf.shape(x))
        drop_prob = (
            tf.math.log(p + eps)
            - tf.math.log(1.0 - p + eps)
            + tf.math.log(unif_noise + eps)
            - tf.math.log(1.0 - unif_noise + eps)
        )
        drop_prob = tf.math.sigmoid(drop_prob / temp)
        random_tensor = 1.0 - drop_prob

        retain_prob = 1.0 - p
        x *= random_tensor
        x /= retain_prob
        return x

    def call(self, inputs, training=None):
        p = tf.math.sigmoid(self.p_logit)

        # initialise regulariser / prior KL term
        input_dim = inputs.shape[-1]  # last dim
        weight = self.layer.kernel
        kernel_regularizer = self.weight_regularizer * tf.reduce_sum(tf.square(weight)) / (1.0 - p)
        dropout_regularizer = p * tf.math.log(p) + (1.0 - p) * tf.math.log(1.0 - p)
        dropout_regularizer *= self.dropout_regularizer * input_dim
        regularizer = tf.reduce_sum(kernel_regularizer + dropout_regularizer)
        if self.is_mc_dropout:
            return self.layer.call(self.concrete_dropout(inputs, p)), regularizer
        else:

            def relaxed_dropped_inputs():
                return self.layer.call(self.concrete_dropout(inputs, p)), regularizer

            return (
                tf.keras.backend.in_train_phase(relaxed_dropped_inputs, self.layer.call(inputs), training=training),
                regularizer,
            )


class NNConcreteDropoutModel(Base_Model):
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
        self.name = "nn_concrete"

        self.earlystopping = callbacks.EarlyStopping(
            monitor="val_loss",
            min_delta=0.001,
            patience=es_patience,
            verbose=0,
            mode="min",
        )

        self.dirname_checkpoint = os.path.join(os.getcwd(), "ML Models", f"{self.name}", "Checkpoints")
        if not os.path.exists(self.dirname_checkpoint):
            os.makedirs(self.dirname_checkpoint)

    @staticmethod
    def mse_loss(true, pred):
        """
        Function to calculate the mean squared error (MSE) during training as a monitoring metric
        """
        n_outputs = pred.shape[1] // 2
        mean = pred[:, :n_outputs]
        return tf.reduce_mean((true - mean) ** 2, -1)

    @staticmethod
    def heteroscedastic_loss(true, pred):
        """
        Function to calculate the heteroscedastic uncertainty during training as the loss function
        """
        n_outputs = pred.shape[1] // 2
        mean = pred[:, :n_outputs]
        log_var = pred[:, n_outputs:]
        precision = tf.math.exp(-log_var)
        return tf.reduce_sum(precision * (true - mean) ** 2.0 + log_var, -1)

    def structure(
        self,
        X_train: np.ndarray,
        Y_train: np.ndarray,
        learning_rate: float,
        hidden_units: int,
        hidden_layers: int,
        act_func: str,
        optimizer: Optimizer,
        dropout_reg: float = 0.001,
        wd: float = 0.0,
    ) -> Model:
        """
        Function that defines the structure of the input, hidden layers, and output required for a concrete dropout neural network model

        Parameters
        ----------
        learning_rate : float type for assigning the learning rate for the optimiser
        hidden_units : int type for the number of hidden units within every hidden layer. Currently, all hidden layers will have this number of hidden units
        hidden_layers : int type for the number of hidden layers in the neural network
        dropout_reg : The dropout regulariser to use in the model
        wd : The weight regulariser to use in the model

        Returns
        -------
        model : The concrete dropout model to fit

        """
        K.clear_session()
        tf.random.set_seed(1)
        tf.random.uniform([1], seed=1)
        losses = []
        inputs = Input(shape=(X_train.shape[1],))
        x = inputs
        for i in range(hidden_layers):
            x, loss = ConcreteDropout(
                Dense(hidden_units, activation=act_func),
                weight_regularizer=wd,
                dropout_regularizer=dropout_reg,
            )(x)
            losses.append(loss)
        mean, loss = ConcreteDropout(
            Dense(Y_train.shape[1]),
            weight_regularizer=wd,
            dropout_regularizer=dropout_reg,
        )(x)
        losses.append(loss)
        log_var, loss = ConcreteDropout(
            Dense(Y_train.shape[1]),
            weight_regularizer=wd,
            dropout_regularizer=dropout_reg,
        )(x)
        losses.append(loss)
        out = concatenate([mean, log_var])
        model = Model(inputs, out)

        for loss in losses:
            model.add_loss(loss)

        model.summary()

        model.compile(
            optimizer=optimizer(learning_rate=learning_rate),
            loss=self.heteroscedastic_loss,
            metrics=[self.mse_loss],
        )
        assert len(model.layers[1].trainable_weights) == 3

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
        max_epochs = int(params.get("max_epochs", 4000))
        act_func = params.get("act_func", "relu")
        optimizer = params.get("optimizer", keras.optimizers.Adam)

        self.filepath = os.path.join(
            self.dirname_checkpoint,
            f"Checkpoint, Concrete Dropout, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.h5",
        )

        self.model = self.structure(
            self.X_train,
            self.Y_train,
            learning_rate,
            hidden_units,
            hidden_layers,
            act_func,
            optimizer,
            dropout_reg=2 / self.X_train.shape[0],
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
            self.Y_train,
            learning_rate,
            hidden_units,
            hidden_layers,
            act_func,
            optimizer,
            dropout_reg=2 / self.X_train.shape[0],
        )
        self.model.load_weights(self.filepath)

    def predict(self, X: np.ndarray, X_transform: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        # The functions below require the data to be a 2D array
        if X.ndim == 1:
            X = X.reshape(1, -1)

        if X_transform:
            if self.variables.num_cat_var > 0:
                X = self.variables.categorical_transform(X).astype("float")
            X = self.transform_only_by_predictor_type(X)

        observed_Y_pred = np.array([self.model.predict(X) for _ in range(10)])
        Y_pred = observed_Y_pred[:, :, :1]
        Y_pred_stddev = np.sqrt(np.exp(observed_Y_pred[:, :, 1:]))

        # Code adapted from:
        #     1. João Caldeira, Brian Nord, Deeply Uncertain: Comparing Methods of Uncertainty Quantification in Deep Learning Algorithms, arXiv:2004.10710, https://github.com/deepskies/DeeplyUncertain-Public,
        #     2. Yarin Gal, Jiri Hron, Alex Kendall, Concrete Dropout, arXiv:1705.07832, https://github.com/yaringal/ConcreteDropout
        Y_val_epistemic_unc = np.std(np.array(Y_pred), axis=0)
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
    #         X,
    #         Y,
    #         model_params,
    #         test_ratio=test_ratio,
    #         sort_before_split=sort_before_split,
    #         **kwargs,
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
        # max_evals = kwargs.get("max_evals", 20)

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
