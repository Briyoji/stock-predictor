import yfinance as yf
from datetime import datetime, timedelta

# from server import TICKERS as STOCK_UNIVERSE
from backend import TICKERS as STOCK_UNIVERSE


def get_latest_close(ticker: str) -> dict:
    """
    Fetch latest available close price (handles weekends/holidays).
    """
    t = yf.Ticker(ticker)

    price = t.fast_info.get("lastPrice") or t.fast_info.get("previousClose")

    if price is None:
        raise ValueError(f"No price data available for {ticker}")

    return {
        "last_close": round(float(price), 2),
        "last_updated": datetime.today().date().isoformat(),
    }

def get_stock_list():
    """
    Returns list of stocks with latest close prices.
    """
    results = []

    for ticker, name in STOCK_UNIVERSE.items():
        try:
            price_data = get_latest_close(ticker)
            results.append(
                {
                    "ticker": ticker,
                    "name": name,
                    **price_data,
                }
            )
        except Exception:
            # Fail soft — do not kill entire endpoint
            continue

    return results

RANGE_TO_DAYS = {
    "1w": 7,
    "1mo": 30,
    "6mo": 180,
    "1y": 365,
    "3y": 365 * 3,
    "5y": 365 * 5,
    "all": None,
}


def get_historical_prices(ticker: str, range_key: str):
    if range_key not in RANGE_TO_DAYS:
        raise ValueError("Invalid range")

    end = datetime.today()

    if RANGE_TO_DAYS[range_key] is None:
        start = "1900-01-01"
    else:
        start = end - timedelta(days=RANGE_TO_DAYS[range_key])
        start = start.strftime("%Y-%m-%d")

    df = yf.download(
        ticker,
        start=start,
        end=end.strftime("%Y-%m-%d"),
        interval="1d",
        progress=False,
        auto_adjust=False,
    )

    if df.empty:
        raise ValueError("No historical data available")

    prices = [
        {
            "date": idx.date().isoformat(),
            "close": round(float(row["Close"].iloc[0]), 2)
        }
        for idx, row in df.iterrows()
    ]

    return prices
