def test_stats_overview(client, auth_headers):
    response = client.get('/stats/overview', headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert 'agents' in data
    assert 'students' in data
    assert 'courses' in data
    assert 'documents' in data
    assert 'executions' in data
    # 4 agents are always registered
    assert data['agents'] == 4


def test_analytics_overview(client, auth_headers):
    response = client.get('/analytics/overview', headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert 'risk_distribution' in data
    assert 'attendance_by_student' in data
    assert 'agent_usage' in data
    assert 'executions_by_day' in data
    assert len(data['executions_by_day']) == 7
    assert set(data['risk_distribution'].keys()) == {'High', 'Medium', 'Low'}
