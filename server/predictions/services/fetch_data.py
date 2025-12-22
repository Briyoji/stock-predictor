import yfinance as yf
from datetime import datetime, timedelta

import pandas as pd

LOOKBACK_TO_DAYS = {
    "short": 20,
    "medium": 60,
    "long": 120,
}


def fetch_lookback_data(ticker: str, lookback: str):
    if lookback not in LOOKBACK_TO_DAYS:
        raise ValueError("Invalid lookback")

    days = LOOKBACK_TO_DAYS[lookback]

    end = datetime.today()
    start = end - timedelta(days=days * 3)  # buffer for non-trading days

    df = yf.download(
        ticker,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    # ---- FIX: Handle MultiIndex columns ----
    if isinstance(df.columns, pd.MultiIndex):
        # Keep only the price field, drop ticker level
        df.columns = df.columns.get_level_values(0)

    if df.empty or len(df) < days + 1:
        raise ValueError("Insufficient historical data")

    # Keep last N+1 rows (for return calculation)
    return df.tail(days + 1)
