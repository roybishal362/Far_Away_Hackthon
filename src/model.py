"""MODEL SLOT — the 'smart core'.

Swap the estimator here (sklearn model, a HuggingFace pipeline, an API call).
Keep `train` / `predict` stable so the UI and evaluation never change.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier


class Model:
    """Thin wrapper so we can swap the underlying brain without touching the app."""

    def __init__(self) -> None:
        # PLACEHOLDER estimator — replace on theme-day.
        self._clf = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X, y) -> "Model":
        self._clf.fit(X, y)
        return self

    def predict(self, X):
        return self._clf.predict(X)

    def predict_proba(self, X):
        return self._clf.predict_proba(X)
