from typing import Tuple

import numpy as np
import sklearn


def remove_nan(X: np.ndarray, Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Removes rows where there are missing objective values. This method allows ML models to be fitted when you have an
    irregular number of Y-values for different objectives

    Parameters
    ----------
    X
    Y

    Returns
    -------

    """
    nan_mask = ~np.isnan(Y)
    return X[nan_mask], Y[nan_mask]


def sort(X: np.ndarray, Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    if len(Y.shape) == 1:
        Y = Y.reshape(-1, 1)

    XY = np.hstack((X, Y))
    XY_sorted = XY[XY[:, X.shape[1]].argsort()]
    X_sorted = XY_sorted[:, :-1]
    Y_sorted = XY_sorted[:, -1].reshape(-1, 1)

    return X_sorted, Y_sorted.flatten()


def train_test_split(array: np.ndarray, splitnum: int) -> Tuple[np.ndarray, np.ndarray]:
    array_test_indexes = [x for x in range(0, array.shape[0], splitnum)]
    array_train_indexes = list(set(list(range(array.shape[0]))) - set(array_test_indexes))

    array_train = array[array_train_indexes]
    array_test = array[array_test_indexes]

    return array_train, array_test


def train_val_test_split(array: np.ndarray, splitnum: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    array_test_indexes = [x for x in range(0, array.shape[0], splitnum)]
    array_val_indexes = [x for x in range(int(splitnum / 2), array.shape[0], splitnum)]
    array_train_indexes = list(set(list(range(array.shape[0]))) - set(array_test_indexes) - set(array_val_indexes))

    array_train = array[array_train_indexes]
    array_val = array[array_val_indexes]
    array_test = array[array_test_indexes]

    return array_train, array_val, array_test


def train_val_test_split_blocks(array: np.ndarray, test_ratio: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    array_train, array_val, array_test = np.split(
        array,
        [
            int((1 - (2 * test_ratio)) * array.shape[0]),
            int((1 - test_ratio) * array.shape[0]),
        ],
    )

    return array_train, array_val, array_test


def shuffle(X: np.ndarray, Y: np.ndarray, seed: int) -> Tuple[np.ndarray, np.ndarray]:
    X, Y = sklearn.utils.shuffle(X, Y, random_state=seed)

    return X, Y


def sort_train_test_split_shuffle(
    X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, seed: int = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    splitnum = int(1 / test_ratio)

    X_sorted, Y_sorted = sort(X, Y)

    X_train, X_test = train_test_split(X_sorted, splitnum)
    Y_train, Y_test = train_test_split(Y_sorted, splitnum)

    if seed == None:
        seed = 1
    # np.random.seed(seed)  # setting the random seed
    X_train, Y_train = shuffle(X_train, Y_train, seed)
    X_test, Y_test = shuffle(X_test, Y_test, seed)

    return X_train, X_test, Y_train, Y_test


def sort_train_val_test_split_shuffle(
    X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, seed: int = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    splitnum = int(1 / test_ratio)

    X_sorted, Y_sorted = sort(X, Y)

    X_train, X_val, X_test = train_val_test_split(X_sorted, splitnum)
    Y_train, Y_val, Y_test = train_val_test_split(Y_sorted, splitnum)

    if seed == None:
        seed = 1
    # np.random.seed(seed)  # setting the random seed
    X_train, Y_train = shuffle(X_train, Y_train, seed)
    X_val, Y_val = shuffle(X_val, Y_val, seed)
    X_test, Y_test = shuffle(X_test, Y_test, seed)

    return X_train, X_val, X_test, Y_train, Y_val, Y_test
