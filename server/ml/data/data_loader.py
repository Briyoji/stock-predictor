# data_loader.py

import yfinance as yf
import pandas as pd


def download_ohlcv(
    ticker: str,
    start: str,
    end: str,
) -> pd.DataFrame:
    """
    Download daily OHLCV data from Yahoo Finance.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    start : str
        Start date in 'YYYY-MM-DD'
    end : str
        End date in 'YYYY-MM-DD'

    Returns
    -------
    pd.DataFrame
        Time-indexed dataframe with columns:
        ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    """

    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        return df

    # ---- FIX: Handle MultiIndex columns ----
    if isinstance(df.columns, pd.MultiIndex):
        # Keep only the price field, drop ticker level
        df.columns = df.columns.get_level_values(0)

    # Standardize column names
    df.columns = [c.strip() for c in list(df.columns)]

    # Ensure datetime index
    df.index = pd.to_datetime(df.index)

    # Sort chronologically (important safeguard)
    df = df.sort_index()

    required_cols = {
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
    }

    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df