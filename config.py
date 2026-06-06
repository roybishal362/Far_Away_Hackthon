"""Central configuration & secret loading for Kakehashi.

Reads keys from environment variables first, then Streamlit secrets (if available).
Importing this module never imports Streamlit at top level, so `core/` stays UI-agnostic.

Honest degradation: if a key is missing, `has(...)` returns False and the relevant
agent/tool reports "not configured" — it NEVER fabricates data.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

try:  # load .env next to this file (gitignored), regardless of cwd
    from pathlib import Path
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except Exception:
    pass


def _get(name: str) -> str | None:
    """Look up a secret: env var wins, then st.secrets, else None."""
    val = os.environ.get(name)
    if val:
        return val
    try:
        import streamlit as st  # imported lazily so core/ never depends on the UI
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return None


@dataclass(frozen=True)
class Settings:
    # LLM (the agents' reasoning brain) — Groq (free, fast, OpenAI-compatible)
    groq_api_key: str | None = None
    llm_model: str = "openai/gpt-oss-120b"  # strong multilingual + reasoning; override via LLM_MODEL

    # Real-data tools
    estat_app_id: str | None = None          # Japan gov statistics (e-Stat)
    jsearch_api_key: str | None = None       # JSearch via OpenWeb Ninja (live jobs)
    amadeus_client_id: str | None = None     # flights
    amadeus_client_secret: str | None = None

    # Privacy
    fernet_key: str | None = None            # AES key for encryption-at-rest (optional)

    def has(self, *names: str) -> bool:
        """True only if every named setting is present."""
        return all(getattr(self, n, None) for n in names)


def load_settings() -> Settings:
    return Settings(
        groq_api_key=_get("GROQ_API_KEY"),
        llm_model=_get("LLM_MODEL") or "openai/gpt-oss-120b",
        estat_app_id=_get("ESTAT_APP_ID"),
        jsearch_api_key=_get("JSEARCH_API_KEY"),
        amadeus_client_id=_get("AMADEUS_CLIENT_ID"),
        amadeus_client_secret=_get("AMADEUS_CLIENT_SECRET"),
        fernet_key=_get("FERNET_KEY"),
    )


SETTINGS = load_settings()
