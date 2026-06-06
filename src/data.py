"""DATA SLOT — how we load & prepare inputs.

Swap the body of `load_data` when the theme drops. Keep the *signature*
stable so the rest of the app doesn't care where data comes from
(CSV, API, upload, generated). That's the 'expansion slot' contract.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    """Return (features X, target y).

    PLACEHOLDER: uses the iris dataset so the app runs today.
    Replace internals on theme-day; keep the return contract.
    """
    bunch = load_iris(as_frame=True)
    X: pd.DataFrame = bunch.data
    y: pd.Series = bunch.target
    return X, y


def summarize(X: pd.DataFrame) -> dict:
    """Quick, honest description of the data we're working with."""
    return {
        "rows": int(len(X)),
        "features": list(X.columns),
        "missing_values": int(X.isna().sum().sum()),
    }
