"""
English: API-level tests for /events/history and /integrations.
Roman Urdu: /events/history aur /integrations ke liye API-level tests.
"""
from backend.app.core.events import event_bus, Event


def test_events_history_requires_auth(client):
    """Unauthenticated call must be rejected."""
    r = client.get('/events/history')
    assert r.status_code == 401


def test_events_history_returns_empty_initially(client, auth_headers):
    # English: Reset the shared bus so the test is deterministic.
    # Roman Urdu: Shared bus reset karo taake test deterministic rahe.
    event_bus._history.clear()
    r = client.get('/events/history', headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body['count'] == 0
    assert body['events'] == []


def test_events_history_shows_published_event(client, auth_headers):
    event_bus._history.clear()
    # Publish with tenant_id=1 (matches conftest's seeded admin)
    event_bus.publish(Event(
        event_type='TestSignal',
        tenant_id=1,
        payload={'k': 'v'},
    ))
    r = client.get('/events/history', headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body['count'] == 1
    assert body['events'][0]['event_type'] == 'TestSignal'
    assert body['events'][0]['payload'] == {'k': 'v'}


def test_events_history_filters_by_tenant(client, auth_headers):
    """Tenant 1 admin must not see events published for tenant 2."""
    event_bus._history.clear()
    event_bus.publish(Event(event_type='E1', tenant_id=1, payload={}))
    event_bus.publish(Event(event_type='E2', tenant_id=999, payload={}))
    r = client.get('/events/history', headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    types = [e['event_type'] for e in body['events']]
    assert 'E1' in types
    assert 'E2' not in types


def test_integrations_list_returns_generic_rest(client, auth_headers):
    r = client.get('/integrations', headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body['count'] >= 1
    names = [i['name'] for i in body['integrations']]
    assert 'generic_rest' in names
    # Each entry must expose an honest status field
    for i in body['integrations']:
        assert i['status'] in (
            'implemented', 'locally_simulated', 'architecture_ready', 'planned'
        )


def test_integration_test_endpoint_returns_honest_failure(client, auth_headers):
    r = client.post('/integrations/generic_rest/test', headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    # The adapter is not configured, so it must report ok=False — no fake success.
    assert body['ok'] is False
    assert 'architecture' in body['message'].lower() or 'configur' in body['message'].lower()


def test_integration_test_unknown_name_returns_not_registered(client, auth_headers):
    r = client.post('/integrations/does_not_exist/test', headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body['ok'] is False
    assert 'not registered' in body['message'].lower()
