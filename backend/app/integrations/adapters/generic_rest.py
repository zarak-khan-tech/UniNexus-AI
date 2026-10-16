# English: Generic REST adapter. Architecture-ready only — no live connection
# until real credentials are configured. Methods raise NotImplementedError
# with a clear message if called before implementation.
# Roman Urdu: Generic REST adapter. Sirf architecture-ready — real credentials
# configure hone tak koi live connection nahi. Methods NotImplementedError
# raise karti hain clear message ke saath agar implementation se pehle call hon.

from typing import Dict, Any, List
from backend.app.integrations.base import (
    IntegrationInterface,
    IntegrationInfo,
    IntegrationStatus,
)


class GenericRESTAdapter(IntegrationInterface):
    """
    English: Adapter for any REST-based university system. Presents a stable
    interface to the platform; the concrete HTTP calls will be added when a
    real integration is scheduled.
    Roman Urdu: Kisi bhi REST-based university system ke liye adapter. Platform
    ko stable interface deta hai; concrete HTTP calls real integration schedule
    hone par add honge.
    """

    def __init__(self, base_url: str = "", api_key: str = "") -> None:
        self.base_url = (base_url or "").strip()
        self.api_key = (api_key or "").strip()

    def info(self) -> IntegrationInfo:
        configured = bool(self.base_url and self.api_key)
        return IntegrationInfo(
            name="generic_rest",
            display_name="Generic REST Integration",
            status=IntegrationStatus.ARCHITECTURE_READY,
            description=(
                "Interface for a REST-based university system. No live connection "
                "is established until credentials are configured by an administrator."
            ),
            capabilities=["test_connection", "fetch_students", "fetch_courses"],
            requires_credentials=True,
            docs_url="",
        )

    def test_connection(self) -> Dict[str, Any]:
        # English: Honest failure. We never claim a fake success.
        # Roman Urdu: Honest failure. Hum fake success claim nahi karte.
        if not self.base_url or not self.api_key:
            return {
                "ok": False,
                "message": (
                    "GenericRESTAdapter is architecture-ready, not live. "
                    "Configure base_url and api_key to activate."
                ),
            }
        raise NotImplementedError(
            "GenericRESTAdapter.test_connection is not implemented against a real "
            "external system. This adapter is a scaffolding for a future integration."
        )

    def fetch_students(self, tenant_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError(
            "GenericRESTAdapter.fetch_students is not implemented. "
            "This adapter is architecture-ready scaffolding only."
        )

    def fetch_courses(self, tenant_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError(
            "GenericRESTAdapter.fetch_courses is not implemented. "
            "This adapter is architecture-ready scaffolding only."
        )


# English: Register this adapter with the global registry on import.
# Roman Urdu: Import pe is adapter ko global registry mein register karo.
from backend.app.integrations.registry import registry  # noqa: E402
registry.register(GenericRESTAdapter())
