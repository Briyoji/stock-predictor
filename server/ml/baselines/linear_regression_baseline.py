# baselines/linear_regression_baseline.py

import numpy as np
from sklearn.linear_model import LinearRegression


class LinearRegressionBaseline:
    def __init__(self):
        self.model = LinearRegression()

    def fit(self, X: np.ndarray, y: np.ndarray):
        X_flat = X.reshape(X.shape[0], -1)
        self.model.fit(X_flat, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        X_flat = X.reshape(X.shape[0], -1)
        return self.model.predict(X_flat)
