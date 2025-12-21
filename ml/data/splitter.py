# splitter.py

import numpy as np
from typing import Tuple


def time_series_split(
    X: np.ndarray,
    y: np.ndarray,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
) -> Tuple[
    Tuple[np.ndarray, np.ndarray],
    Tuple[np.ndarray, np.ndarray],
    Tuple[np.ndarray, np.ndarray],
]:
    """
    Perform a time-based train / val / test split.

    Parameters
    ----------
    X : np.ndarray
        Shape (num_samples, lookback, num_features)
    y : np.ndarray
        Shape (num_samples,)
    train_ratio : float
        Fraction of samples for training
    val_ratio : float
        Fraction of samples for validation

    Returns
    -------
    (X_train, y_train),
    (X_val, y_val),
    (X_test, y_test)
    """

    if len(X) != len(y):
        raise ValueError("X and y must have the same number of samples")

    if train_ratio + val_ratio >= 1.0:
        raise ValueError("train_ratio + val_ratio must be < 1")

    n = len(X)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    X_train, y_train = X[:train_end], y[:train_end]
    X_val, y_val = X[train_end:val_end], y[train_end:val_end]
    X_test, y_test = X[val_end:], y[val_end:]

    return (
        (X_train, y_train),
        (X_val, y_val),
        (X_test, y_test),
    )
