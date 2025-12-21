# scaler_utils.py

import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib


def fit_and_scale(
        split : tuple[
            tuple[np.ndarray, np.ndarray],
            tuple[np.ndarray, np.ndarray],
            tuple[np.ndarray, np.ndarray],
        ],
        idx : int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    
    """
    Fit scaler on training data only and apply to val/test.

    Parameters
    ----------
    split : tuple of train/val/test splits
        Each split is a tuple of (X, y).

    Returns
    -------
    X_train_scaled, X_val_scaled, X_test_scaled, scaler
    """

    (X_train, _), (X_val, _), (X_test, _) = split
    split_map = {0: "short", 1: "medium", 2: "long"}

    n_train, L, F = X_train.shape

    scaler = StandardScaler()

    # Flatten time dimension
    X_train_flat = X_train.reshape(-1, F)
    X_val_flat = X_val.reshape(-1, F)
    X_test_flat = X_test.reshape(-1, F)

    # Fit on train only
    scaler.fit(X_train_flat)

    # Transform
    X_train_scaled = scaler.transform(X_train_flat).reshape(n_train, L, F)
    X_val_scaled = scaler.transform(X_val_flat).reshape(X_val.shape[0], L, F)
    X_test_scaled = scaler.transform(X_test_flat).reshape(X_test.shape[0], L, F)

    # print(X_train_scaled.mean(), X_train_scaled.std())

    save_scaler(scaler, f"./ml/artifacts/{split_map[idx]}/scaler_{split_map[idx]}.pkl")

    return (X_train_scaled,split[0][1]), (X_val_scaled,split[1][1]), (X_test_scaled,split[2][1])


def save_scaler(scaler: StandardScaler, path: str):
    joblib.dump(scaler, path)


def load_scaler(path: str) -> StandardScaler:
    return joblib.load(path)
