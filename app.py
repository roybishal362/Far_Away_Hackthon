"""Far Away — Strike Kit demo app.

Runs end-to-end TODAY with placeholder internals. On theme-day, swap the
slot internals (src/data.py, src/model.py) and this UI keeps working.

Run:  streamlit run app.py
"""
from __future__ import annotations

import streamlit as st
from sklearn.model_selection import train_test_split

from src import data, evaluate
from src.model import Model

st.set_page_config(page_title="Far Away — Strike Kit", page_icon="🚀", layout="wide")

st.title("🚀 Far Away — Strike Kit")
st.caption("Thin app, smart core, proof not claims. Swap the slots when the theme drops.")


@st.cache_data
def _prepare():
    X, y = data.load_data()
    return train_test_split(X, y, test_size=0.25, random_state=42)


@st.cache_resource
def _train(_X_train, _y_train):
    return Model().train(_X_train, _y_train)


X_train, X_test, y_train, y_test = _prepare()
model = _train(X_train, y_train)
y_pred = model.predict(X_test)

# --- PROOF panel: baseline vs us, with real metrics ---
left, right = st.columns(2)

with left:
    st.subheader("📊 The Proof")
    base = evaluate.baseline_accuracy(X_train, y_train, X_test, y_test)
    scores = evaluate.score(y_test, y_pred)
    st.metric("Naive baseline accuracy", f"{base:.1%}")
    st.metric("Our model accuracy", f"{scores['accuracy']:.1%}",
              delta=f"{scores['accuracy'] - base:+.1%} vs baseline")
    st.metric("F1 (macro)", f"{scores['f1_macro']:.3f}")

with right:
    st.subheader("🔍 Where it's right vs wrong")
    st.pyplot(evaluate.confusion_figure(y_test, y_pred))

with st.expander("Data summary (honesty: what are we actually working with?)"):
    st.json(data.summarize(X_train))
