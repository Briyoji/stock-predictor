# feature_engineer.py

import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build causal, time-series features.

    Assumes:
    - DataFrame is sorted by date ascending
    - 'log_return' and 'Volume' columns exist

    Returns:
    - DataFrame with original columns + engineered features
    """

    required_cols = {"log_return", "Volume"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()

    # -----------------------
    # Lagged returns
    # -----------------------
    df["log_return_lag_1"] = df["log_return"].shift(1)
    df["log_return_lag_5"] = df["log_return"].shift(5)

    # -----------------------
    # Rolling means (trend)
    # -----------------------
    df["sma_10"] = df["log_return"].rolling(window=10).mean()
    df["sma_20"] = df["log_return"].rolling(window=20).mean()

    # -----------------------
    # Rolling volatility
    # -----------------------
    df["volatility_10"] = df["log_return"].rolling(window=10).std()
    df["volatility_20"] = df["log_return"].rolling(window=20).std()

    # -----------------------
    # Volume-based features
    # -----------------------
    df["volume_change"] = df["Volume"].pct_change()
    df["volume_sma_20"] = df["Volume"].rolling(window=20).mean()

    # -----------------------
    # Final cleanup
    # -----------------------
    df = df.dropna()

    return df
