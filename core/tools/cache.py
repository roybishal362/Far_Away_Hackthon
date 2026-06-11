"""Tiny thread-safe TTL cache for tool results.

Why: during judging, many people click the same persona chips within minutes.
Caching identical tool queries (a) survives API rate limits/quotas and (b) makes
repeat runs instant. This is a demo-protection layer, not a scaling claim.
"""
from __future__ import annotations

import os
import threading
import time


class TTLCache:
    def __init__(self, ttl_seconds: float | None = None) -> None:
        self.ttl = float(ttl_seconds if ttl_seconds is not None else os.environ.get("TOOL_CACHE_TTL", 600))
        self._data: dict = {}
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            hit = self._data.get(key)
            if not hit:
                return None
            expires, value = hit
            if time.monotonic() > expires:
                del self._data[key]
                return None
            return value

    def set(self, key, value) -> None:
        with self._lock:
            self._data[key] = (time.monotonic() + self.ttl, value)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
