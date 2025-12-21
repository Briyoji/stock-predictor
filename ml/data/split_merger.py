# split_merger.py

import numpy as np

def merge_splits(
    splits: list[
        tuple[
            tuple[np.ndarray, np.ndarray],
            tuple[np.ndarray, np.ndarray],
            tuple[np.ndarray, np.ndarray],
        ]
    ]) -> tuple[
        tuple[np.ndarray, np.ndarray],
        tuple[np.ndarray, np.ndarray],
        tuple[np.ndarray, np.ndarray],
    ]:
    
    """
    Merge multiple train/val/test splits into single splits.

    Parameters
    ----------
    splits : list of tuples
        Each element is a tuple of (train, val, test) splits,
        where each split is a tuple of (X, y).

    Returns
    -------
    Merged (train, val, test) splits.
    """

    X_train = np.concatenate([s[0][0] for s in splits])
    y_train = np.concatenate([s[0][1] for s in splits])

    X_val = np.concatenate([s[1][0] for s in splits])
    y_val = np.concatenate([s[1][1] for s in splits])

    X_test = np.concatenate([s[2][0] for s in splits])
    y_test = np.concatenate([s[2][1] for s in splits])

    return (
        (X_train, y_train),
        (X_val, y_val),
        (X_test, y_test),
    )
