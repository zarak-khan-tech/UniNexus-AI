"""
English: Verify the run_with_timeout utility behaves correctly.
Roman Urdu: run_with_timeout utility sahi kaam karti hai verify karo.
"""
import time
import pytest
from backend.app.core.reliability import run_with_timeout


def test_timeout_completes_quickly():
    """A fast function should return normally."""
    def fast_fn(x):
        return x * 2

    result = run_with_timeout(fast_fn, 2.0, 5)
    assert result == 10


def test_timeout_raises_on_slow_function():
    """A slow function should raise TimeoutError."""
    def slow_fn():
        time.sleep(2.0)
        return "done"

    with pytest.raises(TimeoutError):
        run_with_timeout(slow_fn, 0.5)
