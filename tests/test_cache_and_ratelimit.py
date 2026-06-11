import time

from api.middleware import SlidingWindowLimiter
from core.tools.cache import TTLCache


def test_ttl_cache_hit_and_expiry():
    c = TTLCache(ttl_seconds=0.05)
    c.set("k", 42)
    assert c.get("k") == 42
    time.sleep(0.06)
    assert c.get("k") is None


def test_rate_limiter_blocks_after_limit_and_recovers():
    lim = SlidingWindowLimiter(limit=3, window=60)
    t = 1000.0
    assert all(lim.allow("ip", now=t + i) for i in range(3))
    assert lim.allow("ip", now=t + 3) is False
    assert lim.allow("other-ip", now=t + 3) is True   # per-key isolation
    assert lim.allow("ip", now=t + 61) is True        # window slides
