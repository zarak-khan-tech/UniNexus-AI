# English: Integration base contract. Every external-system adapter (Moodle,
# Canvas, university portal, generic REST) implements this interface.
# Roman Urdu: Integration base contract. Har external-system adapter (Moodle,
# Canvas, university portal, generic REST) is interface ko implement karta hai.

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class IntegrationStatus(str, Enum):
    """
    English: Honest status for every integration. We never claim 'implemented'
    unless the adapter actually talks to a real external system.
    Roman Urdu: Har integration ke liye honest status. Hum 'implemented' claim
    nahi karte jab tak adapter sach mein real external system se baat na kare.
    """
    IMPLEMENTED = "implemented"                # Real, working connector
    LOCALLY_SIMULATED = "locally_simulated"    # Simulated locally, no real external system
    ARCHITECTURE_READY = "architecture_ready"  # Interface exists; credentials required to activate
    PLANNED = "planned"                        # Documented, not yet built


@dataclass
class IntegrationInfo:
    """
    English: Metadata that the frontend/API can safely display without exposing
    credentials or claiming more than we deliver.
    Roman Urdu: Metadata jo frontend/API safely display kar sakti hai, bina
    credentials expose kiye ya jhoota claim kiye.
    """
    name: str
    display_name: str
    status: IntegrationStatus
    description: str
    capabilities: List[str] = field(default_factory=list)
    requires_credentials: bool = True
    docs_url: str = ""


class IntegrationInterface(ABC):
    """
    English: Base class for all integrations. Adapters wrapping real systems
    (Moodle, Canvas, portals) implement this.
    Roman Urdu: Saare integrations ke liye base class. Real systems wrap karne
    wale adapters (Moodle, Canvas, portals) is ko implement karte hain.
    """

    @abstractmethod
    def info(self) -> IntegrationInfo:
        """English: Return metadata about this integration.
        Roman Urdu: Is integration ka metadata return karo."""

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """English: Attempt to connect to the external system. Must NOT fake
        success. Return {'ok': bool, 'message': str}.
        Roman Urdu: External system se connect karne ki koshish. Fake success
        NAHI. {'ok': bool, 'message': str} return karo."""

    @abstractmethod
    def fetch_students(self, tenant_id: int) -> List[Dict[str, Any]]:
        """English: Pull students from the external system.
        Roman Urdu: External system se students pull karo."""

    @abstractmethod
    def fetch_courses(self, tenant_id: int) -> List[Dict[str, Any]]:
        """English: Pull courses from the external system.
        Roman Urdu: External system se courses pull karo."""
