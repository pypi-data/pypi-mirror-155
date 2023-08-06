import sys
from typing import Any, Dict

from keras.models import Model


class SaveModelCheckPoint:
    """
    Class that enables model saving based on both the train loss and validation loss values
    """

    def __init__(self, model: Model, filepath: str):
        """
        Parameters
        ----------
        model : KerasRegressor type object that contains the neural network being trained
        filepath : str type of the file path to save the .h5 file that stores the model parameters

        """
        self.model = model
        self.filepath = filepath
        self.reset()

    def reset(self) -> None:
        """
        Function to reset the variables that are monitored during the check pointing process. This function can be called at the end of model training to allow multiple models to be trained using the same class instantiation of SaveModelCheckPoint
        """
        self.best_epoch = 0
        self.best_loss = sys.float_info.max
        self.best_val_loss = sys.float_info.max

    def save_weights(self, epoch: int, logs: Dict[str, Any]) -> None:
        """
        Function called during the model training procedure when a LambdaCallback is used that allows loss monitoring and model savings.

        Parameters
        ----------
        epoch : int type of the current training epoch
        logs : dict type containing loss information for the current training epoch

        """
        loss = logs["loss"]
        val_loss = logs["val_loss"]

        if epoch == 0:
            for _ in range(10):
                try:
                    self.model.save_weights(self.filepath)  # use TF save_weights method to save best model.
                    break
                except OSError as e:
                    print(e)

        elif loss < self.best_loss and val_loss < self.best_val_loss:
            self.best_loss = loss
            self.best_val_loss = val_loss
            self.best_epoch = epoch
            print(
                f"This epoch's loss ({loss}) and validation loss ({val_loss}) are both the best so far. Saving the model weights.\n"
            )
            for _ in range(10):
                try:
                    self.model.save_weights(self.filepath)  # use TF save_weights method to save best model.
                    break
                except OSError as e:
                    print(e)

        else:
            print(f"Number of epochs since the weights were last saved = {epoch - self.best_epoch}.\n")
