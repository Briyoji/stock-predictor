from ml import load_dataset    

from .zero_baseline import zero_return_baseline
from .linear_regression_baseline import LinearRegressionBaseline
from .metrics import rmse, mae

import numpy as np
from pathlib import Path


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