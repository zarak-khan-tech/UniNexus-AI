def test_list_agents(client, auth_headers):
    response = client.get('/agents/list', headers=auth_headers)
    assert response.status_code == 200
    agents = response.json()['agents']
    names = [a['name'] for a in agents]
    assert 'AttendanceAgent' in names
    assert 'RiskAgent' in names
    assert 'PolicyAgent' in names
    assert 'KnowledgeAgent' in names


def test_run_agent_task_creates_execution(client, auth_headers):
    response = client.post(
        '/agents/run',
        json={'request': 'Show me students with attendance risk'},
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['status'] == 'completed'
    assert 'execution_id' in data
    assert data['execution_id'] > 0
    assert 'execution_plan' in data
    assert len(data['execution_plan']) >= 1
    assert 'execution_results' in data
    assert 'planning_source' in data
    assert data['planning_source'] in ['llm', 'fallback']


def test_executions_audit_log(client, auth_headers):
    # Run two tasks
    client.post('/agents/run', json={'request': 'attendance risk'}, headers=auth_headers)
    client.post('/agents/run', json={'request': 'exam rules'}, headers=auth_headers)

    # Check audit log
    response = client.get('/agents/executions', headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data['total'] >= 2
    for execution in data['executions']:
        assert 'id' in execution
        assert 'user_email' in execution
        assert 'original_request' in execution
        assert 'status' in execution
        assert execution['user_email'] == 'test@test.edu'


def test_llm_status_endpoint(client, auth_headers):
    response = client.get('/agents/llm/status', headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert 'available' in data
