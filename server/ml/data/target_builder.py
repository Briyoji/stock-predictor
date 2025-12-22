# target_builder.py

import pandas as pd
import numpy as np


def add_log_return_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add next-day log return target to the dataframe.

    y_t = log(P_t / P_{t-1})

    Parameters
    ----------
    df : pd.DataFrame
        Must contain 'Adj Close' column
        Indexed by date in ascending order

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'log_return' column
    """

    if "Adj Close" not in df.columns:
        raise ValueError("DataFrame must contain 'Adj Close' column")

    df = df.copy()

    # Compute log return
    df["log_return"] = np.log(df["Adj Close"] / df["Adj Close"].shift(1))

    # Drop the first row (no target available)
    df = df.dropna(subset=["log_return"])

    return df
