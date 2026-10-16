"""
English: Verify the event bus works — pub/sub, isolation, history.
Roman Urdu: Event bus verify karo — pub/sub, isolation, history.
"""
from backend.app.core.events import EventBus, Event

print("=" * 60)
print("Event Bus Tests")
print("=" * 60)

bus = EventBus()
received = []

def handler_a(e):
    received.append(("a", e.payload.get("msg")))

def handler_b(e):
    received.append(("b", e.payload.get("msg")))

def bad_handler(e):
    raise ValueError("intentional failure")

# Test 1: Basic publish/subscribe
bus.subscribe("TestEvent", handler_a)
bus.subscribe("TestEvent", handler_b)
n = bus.publish(Event(event_type="TestEvent", tenant_id=1, payload={"msg": "hello"}))
print(f"Test 1 - Two handlers ran: {n == 2} ({n} ran) -> {'PASS' if n == 2 else 'FAIL'}")

# Test 2: Failing handler doesn't crash others
bus.subscribe("TestEvent", bad_handler)
n = bus.publish(Event(event_type="TestEvent", tenant_id=1, payload={"msg": "world"}))
# 2 good handlers should still have run even though bad_handler failed
print(f"Test 2 - Failure isolated: {n == 2} ({n} ok, 1 failed) -> {'PASS' if n == 2 else 'FAIL'}")

# Test 3: Wildcard subscription
wildcard_hits = []
bus.subscribe("*", lambda e: wildcard_hits.append(e.event_type))
bus.publish(Event(event_type="OtherEvent", tenant_id=1, payload={}))
print(f"Test 3 - Wildcard fired: {len(wildcard_hits) >= 1} -> {'PASS' if wildcard_hits else 'FAIL'}")

# Test 4: History + filter
hist = bus.get_history(event_type="TestEvent", tenant_id=1)
print(f"Test 4 - History filter: {len(hist) == 2} ({len(hist)} events) -> {'PASS' if len(hist) == 2 else 'FAIL'}")

# Test 5: Tenant filter isolates
hist_t2 = bus.get_history(tenant_id=999)
print(f"Test 5 - Tenant filter: {len(hist_t2) == 0} -> {'PASS' if len(hist_t2) == 0 else 'FAIL'}")

print()
print("All event bus tests complete.")
