import numpy as np
import pandas as pd


def build_features(df: pd.DataFrame):
    df = df.copy()

    df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))

    df["sma_10"] = df["Close"].rolling(10).mean()
    df["sma_20"] = df["Close"].rolling(20).mean()
    df["volatility_20"] = df["log_return"].rolling(20).std()

    df = df.dropna()

    features = df[["log_return", "sma_10", "sma_20", "volatility_20"]]

    return features.values
