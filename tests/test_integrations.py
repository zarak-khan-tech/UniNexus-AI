"""
English: Verify the integration interface + registry + generic REST adapter.
Roman Urdu: Integration interface + registry + generic REST adapter verify karo.
"""

import pytest
from backend.app.integrations.base import IntegrationStatus
from backend.app.integrations.registry import IntegrationRegistry
from backend.app.integrations.adapters.generic_rest import GenericRESTAdapter


def test_registry_register_and_list():
    reg = IntegrationRegistry()
    adapter = GenericRESTAdapter()
    reg.register(adapter)
    infos = reg.list()
    assert len(infos) == 1
    assert infos[0].name == "generic_rest"
    assert infos[0].status == IntegrationStatus.ARCHITECTURE_READY
    assert infos[0].requires_credentials is True


def test_registry_get_by_name():
    reg = IntegrationRegistry()
    adapter = GenericRESTAdapter()
    reg.register(adapter)
    got = reg.get("generic_rest")
    assert got is adapter
    assert reg.get("nonexistent") is None


def test_clear_removes_all():
    reg = IntegrationRegistry()
    reg.register(GenericRESTAdapter())
    assert len(reg.list()) == 1
    reg.clear()
    assert len(reg.list()) == 0


def test_test_connection_no_credentials_is_honest():
    """Without credentials, adapter must report ok=False — no fake success."""
    adapter = GenericRESTAdapter()
    result = adapter.test_connection()
    assert result["ok"] is False
    msg = result["message"].lower()
    assert "architecture-ready" in msg or "configured" in msg


def test_fetch_students_raises_not_implemented():
    adapter = GenericRESTAdapter()
    with pytest.raises(NotImplementedError):
        adapter.fetch_students(tenant_id=1)


def test_fetch_courses_raises_not_implemented():
    adapter = GenericRESTAdapter()
    with pytest.raises(NotImplementedError):
        adapter.fetch_courses(tenant_id=1)


def test_global_registry_has_generic_rest():
    """Importing the adapter module registers it globally."""
    from backend.app.integrations.registry import registry
    assert registry.get("generic_rest") is not None
