"""
English: In-memory rate limiter — per-user sliding window. No external 
deps, no Redis. Good enough for single-process FastAPI apps.
Roman Urdu: In-memory rate limiter — per-user sliding window. Koi external 
dep ya Redis nahi. Single-process FastAPI ke liye kaafi hai.
"""
import time
import logging
from collections import defaultdict, deque
from typing import Tuple

logger = logging.getLogger(__name__)


# English: Default limit — 30 requests per 60 seconds per user.
# Roman Urdu: Default limit — 30 requests per 60 seconds per user.
DEFAULT_LIMIT = 30
DEFAULT_WINDOW_SECONDS = 60


class InMemoryRateLimiter:
    """
    English: Simple sliding-window limiter keyed by an arbitrary string 
    (we use the user's email). Old timestamps are pruned on each check.
    Roman Urdu: Simple sliding-window limiter, arbitrary string key ke saath 
    (hum user ka email use karte hain). Har check pe purane timestamps prune 
    hote hain.
    """

    def __init__(self, limit: int = DEFAULT_LIMIT, window_seconds: int = DEFAULT_WINDOW_SECONDS):
        self.limit = limit
        self.window_seconds = window_seconds
        self._buckets: dict[str, deque] = defaultdict(deque)

    def check(self, key: str) -> Tuple[bool, int]:
        """
        English: Returns (allowed, retry_after_seconds). On the first failure 
        retry_after is the seconds until the oldest request in the window 
        expires.
        Roman Urdu: (allowed, retry_after_seconds) return karta hai. Pehli 
        failure pe retry_after woh seconds hain jitne mein purani request 
        window se nikal jayegi.
        """
        now = time.time()
        bucket = self._buckets[key]

        # English: Drop timestamps outside the window.
        # Roman Urdu: Window se bahar wale timestamps hatao.
        cutoff = now - self.window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()

        if len(bucket) >= self.limit:
            retry_after = max(1, int(self.window_seconds - (now - bucket[0])))
            logger.warning(f"Rate limit hit for {key} — retry after {retry_after}s")
            return False, retry_after

        bucket.append(now)
        return True, 0

    def reset(self, key: str) -> None:
        """English: Clear a key's history (useful for tests).
        Roman Urdu: Key ki history clear karo (tests ke liye useful)."""
        self._buckets.pop(key, None)


# English: Single global limiter instance.
# Roman Urdu: Single global limiter instance.
rate_limiter = InMemoryRateLimiter()
