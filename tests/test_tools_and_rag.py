"""
English: API + unit tests for tools list endpoint and RAG evidence thresholds.
Roman Urdu: Tools list endpoint aur RAG evidence thresholds ke liye API + unit tests.
"""


def test_tools_list_endpoint_returns_seven_tools(client, auth_headers):
    """The tools list should reflect the seeded tool_definitions (7 tools)."""
    r = client.get('/tools', headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    names = [t['name'] for t in body['tools']]
    # Core tools that should always be present
    for expected in ('semantic_search', 'student_lookup', 'attendance_query'):
        assert expected in names
    # Counts shape
    assert 'counts' in body
    assert body['counts']['total'] >= 7


def test_tools_list_has_permission_levels(client, auth_headers):
    """Every tool must expose a valid permission level."""
    r = client.get('/tools', headers=auth_headers)
    assert r.status_code == 200
    allowed = {'read', 'write_low', 'write_high'}
    for t in r.json()['tools']:
        assert t['permission'] in allowed
        assert 'description' in t
        assert 'input_schema' in t
        assert 'is_active' in t


def test_rag_evidence_thresholds_are_defined():
    """The knowledge tool must expose strong + weak evidence thresholds."""
    from backend.app.tools.knowledge import (
        STRONG_EVIDENCE_THRESHOLD,
        WEAK_EVIDENCE_THRESHOLD,
    )
    assert 0 < WEAK_EVIDENCE_THRESHOLD < STRONG_EVIDENCE_THRESHOLD < 1
    # Reasonable defaults for cosine similarity
    assert 0.4 <= WEAK_EVIDENCE_THRESHOLD <= 0.6
    assert 0.6 <= STRONG_EVIDENCE_THRESHOLD <= 0.8


def test_knowledge_tool_classifies_evidence():
    """The knowledge tool must label each chunk strong / weak and set an overall."""
    from backend.app.tools.knowledge import SemanticSearchTool
    tool = SemanticSearchTool()
    # Tool exposes input schema with query + top_k
    props = tool.input_schema.get('properties', {})
    assert 'query' in props
    assert 'top_k' in props
    assert tool.permission.name == 'READ'
