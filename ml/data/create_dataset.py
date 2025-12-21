# make_dataset.py

from .get_stock_data import make_stock_data
from .split_merger import merge_splits
from .scaler_utils import fit_and_scale, save_scaler, load_scaler

import numpy as np
from pathlib import Path
import time

from ml import DATASET_DIR

def save_dataset(
    split : tuple[
            tuple[np.ndarray, np.ndarray],
            tuple[np.ndarray, np.ndarray],
            tuple[np.ndarray, np.ndarray],
        ],
    idx : int,
    ):

    """
    Save dataset splits to .npy files.
    Parameters
    ----------
    split : tuple of train/val/test splits
        Each split is a tuple of (X, y).
    idx : int
        Index indicating which dataset (short, medium, long).
    """

    (X_train, y_train), (X_val, y_val), (X_test, y_test) = split
    split_map = {0: "short", 1: "medium", 2: "long"}

    base = DATASET_DIR / split_map[idx]
    base.mkdir(parents=True, exist_ok=True)

    np.save(base / "X_train.npy", X_train)
    np.save(base / "y_train.npy", y_train)
    np.save(base / "X_val.npy", X_val)
    np.save(base / "y_val.npy", y_val)
    np.save(base / "X_test.npy", X_test)
    np.save(base / "y_test.npy", y_test)


def create_datasets(tickers : list[str] = None, start: str = "2014-01-01", end: str = "2024-12-31"):


    tickers = ["AAPL", "MSFT", "GOOGL"] if tickers is None else tickers

    splits = [[],[],[]] # short, medium, long
    # short_splits = []
    # medium_splits = []
    # long_splits = []

    s_time = time.time()

    for ticker in tickers:
        short, medium, long = make_stock_data(
            ticker=ticker,
            start=start,
            end=end,
        )

        # short_splits.append(short)
        # medium_splits.append(medium)
        # long_splits.append(long)

        splits[0].append(short)
        splits[1].append(medium)
        splits[2].append(long)

    download_time = time.time() - s_time
    print(f"[DATA] : Downloaded all stock data in {download_time:.2f} seconds.")

    # short_data  = merge_splits(short_splits)
    # medium_data = merge_splits(medium_splits)
    # long_data   = merge_splits(long_splits)

    s_time = time.time()
    merged_splits = [merge_splits(s) for s in splits]

    merge_time = time.time() - s_time
    print(f"[MERGE] : Merged all stock data in {merge_time:.2f} seconds.")

    
    s_time = time.time()
    scaled_splits = [fit_and_scale(s, i) for i, s in enumerate(merged_splits)]
    
    scale_time = time.time() - s_time
    print(f"[SCALE] : Scaled all stock data in {scale_time:.2f} seconds.")

    for i, s in enumerate(scaled_splits) : 
        save_dataset(s, i)
