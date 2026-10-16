"""
English: Verify rate limiter behaves correctly.
Roman Urdu: Rate limiter sahi behave karta hai verify karo.
"""
import time
from backend.app.core.rate_limit import InMemoryRateLimiter

print("=" * 70)
print("Rate Limiter Tests")
print("=" * 70)

# Test 1: Allows up to limit
lim = InMemoryRateLimiter(limit=5, window_seconds=60)
results = [lim.check('user1')[0] for _ in range(5)]
print(f"Test 1 - First 5 requests allowed: {all(results)} → {'PASS' if all(results) else 'FAIL'}")

# Test 2: Blocks 6th request
allowed, retry_after = lim.check('user1')
print(f"Test 2 - 6th request blocked: {not allowed} (retry_after={retry_after}s) → {'PASS' if not allowed else 'FAIL'}")

# Test 3: Different user is unaffected
allowed2, _ = lim.check('user2')
print(f"Test 3 - user2 still allowed: {allowed2} → {'PASS' if allowed2 else 'FAIL'}")

# Test 4: Window expiry (short window)
lim2 = InMemoryRateLimiter(limit=2, window_seconds=1)
lim2.check('user3'); lim2.check('user3')
blocked, _ = lim2.check('user3')
print(f"Test 4 - 3rd request blocked immediately: {not blocked} → {'PASS' if blocked else 'FAIL'}")
time.sleep(1.2)
allowed3, _ = lim2.check('user3')
print(f"Test 5 - After window expiry allowed: {allowed3} → {'PASS' if allowed3 else 'FAIL'}")

print()
print("All rate limiter tests complete.")
