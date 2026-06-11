"""LLM client — Groq (free, fast, OpenAI-compatible). The agents' reasoning brain.

Usage:
    from core.llm import get_llm
    llm = get_llm()
    text = llm.complete(system="...", user="...")
    obj  = llm.json(system="...", user="...")   # structured output for agents

Honesty: if GROQ_API_KEY is missing, calls raise LLMNotConfigured — we never
silently fabricate a response.

Key failover: if GROQ_API_KEY_FALLBACK is set, a rate-limit (429) on the primary
key transparently retries on the fallback key — roughly doubling daily free-tier
quota. The proper long-term fix is the Groq Dev tier.
"""
from __future__ import annotations

import json

from config import SETTINGS


class LLMNotConfigured(RuntimeError):
    pass


def _is_rate_limit(exc: Exception) -> bool:
    s = str(exc).lower()
    return "rate_limit" in s or "rate limit" in s or "429" in s


class LLM:
    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self.model = model or SETTINGS.llm_model
        self.api_key = api_key or SETTINGS.groq_api_key
        self.fallback_key = SETTINGS.groq_api_key_fallback

    def available(self) -> bool:
        return bool(self.api_key)

    def _keys(self) -> list[str]:
        return [k for k in (self.api_key, self.fallback_key) if k]

    def _create(self, **kwargs):
        """Create a chat completion, failing over to the backup key on a rate-limit."""
        keys = self._keys()
        if not keys:
            raise LLMNotConfigured("GROQ_API_KEY not configured")
        from groq import Groq
        last: Exception | None = None
        for key in keys:
            try:
                return Groq(api_key=key).chat.completions.create(**kwargs)
            except Exception as exc:  # noqa: BLE001
                last = exc
                if _is_rate_limit(exc):
                    continue  # primary quota hit — try the next key
                raise
        raise last  # type: ignore[misc]  # all keys rate-limited

    def complete(self, system: str, user: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        resp = self._create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""

    def json(self, system: str, user: str, temperature: float = 0.1, max_tokens: int = 2048) -> dict:
        """Structured output. Groq supports OpenAI-style JSON mode."""
        resp = self._create(
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
            start, end = raw.find("{"), raw.rfind("}")
            return json.loads(raw[start : end + 1]) if start != -1 and end != -1 else {}


_LLM: LLM | None = None


def get_llm() -> LLM:
    global _LLM
    if _LLM is None:
        _LLM = LLM()
    return _LLM
