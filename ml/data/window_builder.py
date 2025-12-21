# window_builder.py

import numpy as np
import pandas as pd
from typing import Tuple


def build_windows(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str,
    lookback: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build sliding windows for time-series modeling.

    Parameters
    ----------
    df : pd.DataFrame
        Feature dataframe sorted by time ascending
    feature_cols : list[str]
        Columns to use as model inputs
    target_col : str
        Target column name (e.g., 'log_return')
    lookback : int
        Number of past timesteps per sample

    Returns
    -------
    X : np.ndarray
        Shape: (num_samples, lookback, num_features)
    y : np.ndarray
        Shape: (num_samples,)
    """

    if lookback <= 0:
        raise ValueError("lookback must be positive")

    for col in feature_cols + [target_col]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    values_X = df[feature_cols].values
    values_y = df[target_col].values

    X, y = [], []

    for t in range(lookback, len(df)):
        X.append(values_X[t - lookback : t])
        y.append(values_y[t])

    X = np.array(X)
    y = np.array(y)

    if len(X) == 0:
        raise ValueError("No samples created — check lookback or data length")

    return X, y
