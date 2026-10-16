"""
English: Proper pytest suite for the event bus.
Roman Urdu: Event bus ke liye proper pytest suite.
"""
from backend.app.core.events import EventBus, Event


def test_subscribe_and_publish():
    bus = EventBus()
    hits = []
    bus.subscribe("TestEvent", lambda e: hits.append(e.payload["msg"]))
    n = bus.publish(Event(event_type="TestEvent", tenant_id=1, payload={"msg": "hi"}))
    assert n == 1
    assert hits == ["hi"]


def test_multiple_handlers_all_fire():
    bus = EventBus()
    hits = []
    bus.subscribe("E", lambda e: hits.append("a"))
    bus.subscribe("E", lambda e: hits.append("b"))
    n = bus.publish(Event(event_type="E", tenant_id=1, payload={}))
    assert n == 2
    assert sorted(hits) == ["a", "b"]


def test_handler_exception_is_isolated():
    bus = EventBus()
    hits = []
    bus.subscribe("E", lambda e: hits.append("ok"))

    def bad(e):
        raise ValueError("boom")

    bus.subscribe("E", bad)
    n = bus.publish(Event(event_type="E", tenant_id=1, payload={}))
    # Only the good handler should have been counted as successful.
    assert n == 1
    assert hits == ["ok"]


def test_wildcard_subscriber_receives_all():
    bus = EventBus()
    got = []
    bus.subscribe("*", lambda e: got.append(e.event_type))
    bus.publish(Event(event_type="A", tenant_id=1, payload={}))
    bus.publish(Event(event_type="B", tenant_id=1, payload={}))
    assert "A" in got and "B" in got


def test_history_filtered_by_tenant():
    bus = EventBus()
    bus.publish(Event(event_type="E", tenant_id=1, payload={}))
    bus.publish(Event(event_type="E", tenant_id=2, payload={}))
    bus.publish(Event(event_type="E", tenant_id=1, payload={}))
    t1 = bus.get_history(event_type="E", tenant_id=1)
    t2 = bus.get_history(event_type="E", tenant_id=2)
    assert len(t1) == 2
    assert len(t2) == 1


def test_history_max_length_enforced():
    bus = EventBus(max_history=3)
    for i in range(10):
        bus.publish(Event(event_type="E", tenant_id=1, payload={"i": i}))
    hist = bus.get_history(tenant_id=1, limit=100)
    assert len(hist) == 3
    # Should keep the most recent 3
    assert [h.payload["i"] for h in hist] == [7, 8, 9]
