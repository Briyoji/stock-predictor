# utils.py

"""
Utility Data for ML Pipeline
"""

from pathlib import Path

FEATURE_COLS = [
    "log_return_lag_1",
    "log_return_lag_5",
    "sma_10",
    "sma_20",
    "volatility_10",
    "volatility_20",
    "volume_change",
    "volume_sma_20",
]

DATASET_DIR = Path("./ml/data/datasets/")