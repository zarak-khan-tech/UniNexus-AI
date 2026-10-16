# English: In-process event bus — pub/sub for system events. No Redis/Kafka.
# Roman Urdu: In-process event bus — system events ke liye pub/sub. Redis/Kafka nahi.

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """English: A structured system event.
    Roman Urdu: Ek structured system event."""
    event_type: str
    tenant_id: int
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class EventBus:
    """
    English: Simple in-process pub/sub. Handlers run synchronously;
    exceptions in one handler do not affect others.
    Roman Urdu: Simple in-process pub/sub. Handlers synchronously chalte hain;
    ek handler ki exception doosre ko affect nahi karti.
    """

    def __init__(self, max_history: int = 200):
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = defaultdict(list)
        self._history: List[Event] = []
        self._max_history = max_history

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """English: Register a handler for an event type. Use '*' for all events.
        Roman Urdu: Ek event type ke liye handler register karo. '*' sab ke liye."""
        self._subscribers[event_type].append(handler)
        logger.info(f"[events] subscribed {handler.__name__} to '{event_type}'")

    def publish(self, event: Event) -> int:
        """
        English: Publish an event. Returns the number of handlers that ran successfully.
        Roman Urdu: Event publish karo. Kitne handlers successfully chale woh return karo.
        """
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

        handlers = list(self._subscribers.get(event.event_type, [])) + \
                   list(self._subscribers.get("*", []))

        ok = 0
        for handler in handlers:
            try:
                handler(event)
                ok += 1
            except Exception as e:
                logger.error(
                    f"[events] handler {getattr(handler, '__name__', 'anon')} "
                    f"failed for '{event.event_type}': {e}"
                )
        return ok

    def get_history(
        self,
        event_type: Optional[str] = None,
        tenant_id: Optional[int] = None,
        limit: int = 50,
    ) -> List[Event]:
        """English: Return recent events, optionally filtered.
        Roman Urdu: Recent events return karo, optionally filtered."""
        filtered = self._history
        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]
        if tenant_id is not None:
            filtered = [e for e in filtered if e.tenant_id == tenant_id]
        return filtered[-limit:]


# English: Single global event bus instance.
# Roman Urdu: Single global event bus instance.
event_bus = EventBus()
