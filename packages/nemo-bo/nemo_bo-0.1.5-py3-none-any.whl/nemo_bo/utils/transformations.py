import math
from typing import List

import numpy as np
from numba import cuda
from sklearn.preprocessing import MinMaxScaler, PowerTransformer, StandardScaler


class Transformations:
    def standardscaler(self, data: np.ndarray) -> np.ndarray:
        """
        Standardises the data by utilising sklearn.preprocessing.StandardScaler to transform the data such that its distribution will have a mean value 0 and standard deviation of 1
        For multivariate data, this is done feature-wise, i.e. independently for each column of the data

        Parameters
        ----------
        data : array-like with shape (n_samples, n_features) containing the data used to compute the mean and standard deviation used for later scaling along the features axis.

        Returns
        -------
        data_standardised : numpy.ndarray type of standardised data
        scaler.mean_ :  numpy.ndarray type array containing the mean of each feature for multivariate data, or the mean of all the features for 1D arrays of data
        scaler.scale_ : numpy.ndarray type array containing the standard deviation of each feature for multivariate data, or the standard deviation of all the features for 1D arrays of data

        """

        if data.ndim == 1:
            data = data.reshape(-1, 1)
        self.scaler = StandardScaler()
        data_standardised = self.scaler.fit_transform(data)

        return data_standardised

    def standardscaler_transform_only(self, data: np.ndarray) -> np.ndarray:
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        data_standardised = self.scaler.transform(data)

        return data_standardised

    def inverse_standardscaler(self, data_standardised: np.ndarray) -> np.ndarray:
        if len(data_standardised.shape) == 1:
            data_standardised = data_standardised.reshape(-1, 1)
        data = self.scaler.inverse_transform(data_standardised)

        return data

    def minmaxscaler(self, data: np.ndarray) -> np.ndarray:
        """
        Standardises the data by utilising sklearn.preprocessing.MinMaxScaler to transform the data by scaling and translating each feature individually such that it is in the given range on the training set, e.g. between zero and one
        For multivariate data, this is done feature-wise, i.e. independently for each column of the data

        Parameters
        ----------
        data : array-like with shape (n_samples, n_features) containing the data used to compute the mean and standard deviation used for later scaling along the features axis.

        Returns
        -------
        data_standardised : numpy.ndarray type of standardised data
        scaler.mean_ :  numpy.ndarray type array containing the mean of each feature for multivariate data, or the mean of all the features for 1D arrays of data
        scaler.scale_ : numpy.ndarray type array containing the standard deviation of each feature for multivariate data, or the standard deviation of all the features for 1D arrays of data

        """

        if data.ndim == 1:
            data = data.reshape(-1, 1)
        self.scaler = MinMaxScaler()
        data_normalised = self.scaler.fit_transform(data)

        return data_normalised

    def minmaxscaler_transform_only(self, data: np.ndarray) -> np.ndarray:
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        data_normalised = self.scaler.transform(data)

        return data_normalised

    def inverse_minmaxscaler(self, data_normalised: np.ndarray) -> np.ndarray:
        if len(data_normalised.shape) == 1:
            data_normalised = data_normalised.reshape(-1, 1)
        data = self.scaler.inverse_transform(data_normalised)

        return data

    def yeo_johnson_power_transform(self, data: np.ndarray) -> np.ndarray:
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        self.scaler = StandardScaler()
        data_standardised = self.scaler.fit_transform(data)

        self.powertransform = PowerTransformer(method="yeo-johnson")
        data_standardised_transform = self.powertransform.fit_transform(data_standardised)

        return data_standardised_transform

    def inverse_yeo_johnson_power_transform(self, data_standardised_transform: np.ndarray) -> np.ndarray:
        data_standardised = self.powertransform.inverse_transform(data_standardised_transform)
        data = self.scaler.inverse_transform(data_standardised)

        return data

    def numba_cuda_1d_kernel(self, array: np.ndarray) -> None:
        # Kernel declaration and invocation for a 1D array and grid of threads
        # The number of threads to assign to each block when instantiating the kernel
        self.threadsperblock1d = 1024
        # Defines number of thread blocks on the grid
        self.blockspergrid1d = (array.shape[0] + (self.threadsperblock1d - 1)) // self.threadsperblock1d

    def numba_cuda_2d_kernel(self, array: np.ndarray) -> None:
        # Kernel declaration and invocation for a 2D array and grid of threads
        # The number of threads to assign to each block when instantiating the kernel. Each value of 32 is equal to the square root of the maximum number of threads per block on the computer. In this case the square root of 1024
        self.threadsperblock2d = (
            32,
            32,
        )
        # Number of thread blocks in the x direction. FYI: The product of the number of thread blocks (or “blocks per grid”) and a number of threads per block will give the total number of threads launched.
        blockspergrid_x = math.ceil(array.shape[0] / self.threadsperblock2d[0])
        # Number of thread blocks in the y direction.
        blockspergrid_y = math.ceil(array.shape[1] / self.threadsperblock2d[1])
        # Defines number of thread blocks on the xy grid
        self.blockspergrid2d = (
            blockspergrid_x,
            blockspergrid_y,
        )

    def X_min_max_norm_cuda_run(
        self, X: np.ndarray, x_max: List[int | float] | np.ndarray, x_min: List[int | float] | np.ndarray
    ) -> np.ndarray:
        X_norm = np.zeros_like(X)
        self.numba_cuda_2d_kernel(X)
        self.X_min_max_norm_cuda[self.blockspergrid2d, self.threadsperblock2d](X, X_norm, x_max, x_min)

        return X_norm

    @staticmethod
    @cuda.jit
    def X_min_max_norm_cuda(
        X: np.ndarray, X_norm: np.ndarray, x_max: List[int | float] | np.ndarray, x_min: List[int | float] | np.ndarray
    ) -> None:
        # Normalise the features by applying min-max feature scaling
        # Increments through a 2D grid
        x, y = cuda.grid(2)
        if x < X.shape[0] and y < X.shape[1]:
            X_norm[x, y] = (X[x][y] - x_min[y]) / (x_max[y] - x_min[y])

    def X_inverse_min_max_norm_cuda_run(
        self, X_norm: np.ndarray, x_max: List[int | float] | np.ndarray, x_min: List[int | float] | np.ndarray
    ) -> np.ndarray:
        X = np.zeros_like(X_norm)
        self.numba_cuda_2d_kernel(X_norm)
        self.X_inverse_min_max_norm_cuda[self.blockspergrid2d, self.threadsperblock2d](X_norm, X, x_max, x_min)

        return X

    @staticmethod
    @cuda.jit
    def X_inverse_min_max_norm_cuda(
        X_norm: np.ndarray, X: np.ndarray, x_max: List[int | float] | np.ndarray, x_min: List[int | float] | np.ndarray
    ):
        # Un-normalise the features by reversing the min-max feature scaling
        # Increments through a 2D grid
        x, y = cuda.grid(2)
        if x < X_norm.shape[0] and y < X_norm.shape[1]:
            X[x, y] = (X_norm[x][y] * (x_max[y] - x_min[y])) + x_min[y]

    def X_standardisation_cuda_run(
        self, X: np.ndarray, X_mean: List[int | float] | np.ndarray, X_stddev: List[int | float] | np.ndarray
    ) -> np.ndarray:
        X_standardised = np.zeros_like(X)
        self.numba_cuda_2d_kernel(X)
        self.X_standardisation_cuda[self.blockspergrid2d, self.threadsperblock2d](X, X_standardised, X_mean, X_stddev)

        return X_standardised

    @staticmethod
    @cuda.jit
    def X_standardisation_cuda(
        X: np.ndarray,
        X_standardised: np.ndarray,
        X_mean: List[int | float] | np.ndarray,
        X_stddev: List[int | float] | np.ndarray,
    ) -> None:
        # Increments through a 2D grid
        x, y = cuda.grid(2)
        if x < X.shape[0] and y < X.shape[1]:
            X_standardised[x, y] = (X[x][y] - X_mean[y]) / X_stddev[y]

    def Y_standardisation_cuda_run(self, Y: np.ndarray, Y_mean: int | float, Y_stddev: int | float) -> np.ndarray:
        if len(Y.shape) > 1:
            Y = Y.flatten()

        Y_standardised = np.zeros_like(Y)
        self.numba_cuda_1d_kernel(Y)
        self.Y_standardisation_cuda[self.blockspergrid1d, self.threadsperblock1d](Y, Y_standardised, Y_mean, Y_stddev)

        return Y_standardised

    @staticmethod
    @cuda.jit
    def Y_standardisation_cuda(
        Y: np.ndarray, Y_standardised: np.ndarray, Y_mean: int | float, Y_stddev: int | float
    ) -> None:
        # Increments through a 1D grid
        x = cuda.grid(1)
        if x < Y.shape[0]:
            Y_standardised[x] = (Y[x] - Y_mean) / Y_stddev

    def Y_inverse_standardisation_cuda_run(
        self, Y_standardised: np.ndarray, Y_mean: int | float, Y_stddev: int | float
    ) -> np.ndarray:
        if len(Y_standardised.shape) > 1:
            Y_standardised = Y_standardised.flatten()

        Y = np.zeros_like(Y_standardised)
        self.numba_cuda_1d_kernel(Y_standardised)
        self.Y_inverse_standardisation_cuda[self.blockspergrid1d, self.threadsperblock1d](
            Y_standardised, Y, Y_mean, Y_stddev
        )

        return Y

    @staticmethod
    @cuda.jit
    def Y_inverse_standardisation_cuda(
        Y_standardised: np.ndarray, Y: np.ndarray, Y_mean: int | float, Y_stddev: int | float
    ) -> None:
        # Increments through a 1D grid
        x = cuda.grid(1)
        if x < Y.shape[0]:
            Y[x] = (Y_standardised[x] * Y_stddev) + Y_mean
