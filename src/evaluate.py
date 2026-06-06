"""EVALUATION SLOT — our differentiator: PROOF, not claims.

Every claim the demo makes should trace back to a number or chart here:
a baseline to beat, real metrics, and a visual. Judges' silent question is
'is this real?' — this module answers it.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")  # headless backend for Streamlit
import matplotlib.pyplot as plt
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score


def baseline_accuracy(X_train, y_train, X_test, y_test) -> float:
    """The 'dumb' score to beat — proves our model adds real value."""
    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    return float(accuracy_score(y_test, dummy.predict(X_test)))


def score(y_true, y_pred) -> dict:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
    }


def confusion_figure(y_true, y_pred):
    """Visual evidence of where the model is right vs wrong."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4, 4))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    for (i, j), v in np.ndenumerate(cm):
        ax.text(j, i, str(v), ha="center", va="center")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    return fig
