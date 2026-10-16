# English: Integration registry — stores registered adapters by name.
# Roman Urdu: Integration registry — registered adapters ko name ke saath store karta hai.

from typing import Dict, List, Optional
from backend.app.integrations.base import IntegrationInterface, IntegrationInfo


class IntegrationRegistry:
    """
    English: Simple in-memory registry. Adapters register themselves at import
    time (or explicitly), and the API/frontend can list them.
    Roman Urdu: Simple in-memory registry. Adapters import time pe khud register
    hote hain (ya explicitly), aur API/frontend unhe list kar sakti hain.
    """

    def __init__(self) -> None:
        self._adapters: Dict[str, IntegrationInterface] = {}

    def register(self, adapter: IntegrationInterface) -> None:
        """English: Register an adapter. Overwrites any existing one with same name.
        Roman Urdu: Adapter register karo. Same name wale ko overwrite karta hai."""
        info = adapter.info()
        self._adapters[info.name] = adapter

    def unregister(self, name: str) -> None:
        self._adapters.pop(name, None)

    def list(self) -> List[IntegrationInfo]:
        """English: Return metadata for all registered integrations.
        Roman Urdu: Saare registered integrations ka metadata return karo."""
        return [a.info() for a in self._adapters.values()]

    def get(self, name: str) -> Optional[IntegrationInterface]:
        """English: Lookup an adapter by name.
        Roman Urdu: Name se adapter lookup karo."""
        return self._adapters.get(name)

    def clear(self) -> None:
        """English: Remove all adapters (used in tests).
        Roman Urdu: Saare adapters hatao (tests mein use hota hai)."""
        self._adapters.clear()


# English: Single global registry instance.
# Roman Urdu: Single global registry instance.
registry = IntegrationRegistry()
