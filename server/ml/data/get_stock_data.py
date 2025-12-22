# get_stock_data.py

from .data_loader import download_ohlcv
from .target_builder import add_log_return_target
from .feature_engineer import build_features
from .window_builder import build_windows
from .splitter import time_series_split

from server.ml import FEATURE_COLS

import pandas as pd
import numpy as np

# FEATURE_COLS = [
#     "log_return_lag_1",
#     "log_return_lag_5",
#     "sma_10",
#     "sma_20",
#     "volatility_10",
#     "volatility_20",
#     "volume_change",
#     "volume_sma_20",
# ]

def make_stock_data(ticker: str, start: str = "2014-01-01", end: str = "2024-12-31") \
    -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:

    """
    Get processed stock data ready for modeling.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., 'AAPL')  
    start : str
        Start date (YYYY-MM-DD)
    end : str
        End date (YYYY-MM-DD)

    Returns
    -------
    tuple of train/val/test splits for short, medium, and long lookbacks
    """
    df = download_ohlcv(
        ticker=ticker,
        start=start,
        end=end,
    )

    if df.empty:
        return (([],[]), ([],[]), ([],[]))

    df = add_log_return_target(df)
    df = build_features(df)
    
    X_short, y_short = build_windows(
        df=df,
        feature_cols=FEATURE_COLS,
        target_col="log_return",
        lookback=20,
    )

    X_med, y_med = build_windows(
        df=df,
        feature_cols=FEATURE_COLS,
        target_col="log_return",
        lookback=60,
    )

    X_long, y_long = build_windows(
        df=df,
        feature_cols=FEATURE_COLS,
        target_col="log_return",
        lookback=120,
    )

    return (
        time_series_split(X_short, y_short), 
        time_series_split(X_med, y_med), 
        time_series_split(X_long, y_long)
    )