"""Per-IP sliding-window rate limiting (stdlib only — no new dependencies).

Demo-protection: a single judge clicking around stays far under the limit, but a
stuck retry-loop or a scraper can't burn the free-tier LLM/API quotas that the
live demo depends on. Tune with RATE_LIMIT_PER_MIN (default 40); /health is exempt.
"""
from __future__ import annotations

import os
import threading
import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

EXEMPT_PATHS = {"/health"}


class SlidingWindowLimiter:
    """Allow at most `limit` hits per `window` seconds per key. Thread-safe."""

    def __init__(self, limit: int, window: float = 60.0) -> None:
        self.limit, self.window = limit, window
        self._hits: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, key: str, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        with self._lock:
            dq = self._hits[key]
            cutoff = now - self.window
            while dq and dq[0] <= cutoff:
                dq.popleft()
            if len(dq) >= self.limit:
                return False
            dq.append(now)
            return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int | None = None) -> None:
        super().__init__(app)
        self.limiter = SlidingWindowLimiter(
            limit=int(limit if limit is not None else os.environ.get("RATE_LIMIT_PER_MIN", 40)))

    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXEMPT_PATHS or request.method == "OPTIONS":
            return await call_next(request)
        ip = request.client.host if request.client else "unknown"
        if not self.limiter.allow(ip):
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests — please wait a minute and try again."},
            )
        return await call_next(request)
