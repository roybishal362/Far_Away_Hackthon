"""LLM client — Groq (free, fast, OpenAI-compatible). The agents' reasoning brain.

Usage:
    from core.llm import get_llm
    llm = get_llm()
    text = llm.complete(system="...", user="...")
    obj  = llm.json(system="...", user="...")   # structured output for agents

Honesty: if GROQ_API_KEY is missing, calls raise LLMNotConfigured — we never
silently fabricate a response.
"""
from __future__ import annotations

import json

from config import SETTINGS


class LLMNotConfigured(RuntimeError):
    pass


class LLM:
    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self.model = model or SETTINGS.llm_model
        self.api_key = api_key or SETTINGS.groq_api_key

    def available(self) -> bool:
        return bool(self.api_key)

    def _client(self):
        if not self.api_key:
            raise LLMNotConfigured("GROQ_API_KEY not configured — set it in Streamlit secrets")
        from groq import Groq
        return Groq(api_key=self.api_key)

    def complete(self, system: str, user: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        resp = self._client().chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""

    def json(self, system: str, user: str, temperature: float = 0.1, max_tokens: int = 2048) -> dict:
        """Structured output. Groq supports OpenAI-style JSON mode."""
        resp = self._client().chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system + "\n\nRespond with ONLY a single valid JSON object."},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Last-resort: salvage the first {...} block. Better to surface than to crash a demo.
            start, end = raw.find("{"), raw.rfind("}")
            return json.loads(raw[start : end + 1]) if start != -1 and end != -1 else {}


_LLM: LLM | None = None


def get_llm() -> LLM:
    global _LLM
    if _LLM is None:
        _LLM = LLM()
    return _LLM
