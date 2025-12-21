# baselines/zero_baseline.py

import numpy as np


def zero_return_baseline(y_true: np.ndarray) -> np.ndarray:
    return np.zeros_like(y_true)
