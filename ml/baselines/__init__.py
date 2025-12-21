
from .zero_baseline import zero_return_baseline
from .linear_regression_baseline import LinearRegressionBaseline
from .metrics import rmse, mae

import numpy as np
from pathlib import Path

from ml import FEATURE_COLS, DATASET_DIR as base_dir

def load_dataset(dataset_lookback: str) -> tuple[
        tuple[np.ndarray, np.ndarray],
        tuple[np.ndarray, np.ndarray],
        tuple[np.ndarray, np.ndarray],
    ]:

    """
    Load train/val/test splits from disk.

    Parameters
    ----------
    dataset_lookback : str
        One of "short", "medium", "long" indicating which dataset to load.

    Returns
    -------
    (X_train, y_train), (X_val, y_val), (X_test, y_test)
    """

    base = base_dir / dataset_lookback

    X_train = np.load(base / "X_train.npy")
    y_train = np.load(base / "y_train.npy")

    X_val = np.load(base / "X_val.npy")
    y_val = np.load(base / "y_val.npy")

    X_test = np.load(base / "X_test.npy")
    y_test = np.load(base / "y_test.npy")

    return (
        (X_train, y_train),
        (X_val, y_val),
        (X_test, y_test),
    )
    

def main():

    datasets_pth = {
        0 : "short",
        1: "medium",
        2: "long",
    }

    # Load dataset
    short_data = load_dataset(datasets_pth[0])
    medium_data = load_dataset(datasets_pth[1])
    long_data = load_dataset(datasets_pth[2])

    datasets = [short_data, medium_data, long_data]

    for idx, dataset in enumerate(datasets):
        print("="*5, datasets_pth[idx].upper(), "DATASET BASELINES", "="*5)
        (X_train, y_train), (X_val, y_val), (X_test, y_test) = dataset

        # ---- Zero baseline ----
        y_pred_zero = zero_return_baseline(y_test)
        print("Zero RMSE:", rmse(y_test, y_pred_zero))

        # ---- Linear regression baseline ----
        lr = LinearRegressionBaseline()
        lr.fit(X_train, y_train)

        y_pred_lr = lr.predict(X_test)
        print("Linear RMSE:", rmse(y_test, y_pred_lr), end="\n\n")

if __name__ == "__main__":
    main()