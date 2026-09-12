def test_register_user(client):
    response = client.post('/auth/register', json={
        'email': 'newuser@test.edu',
        'password': 'newpassword123',
        'role': 'faculty',
        'tenant_id': 1,
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['email'] == 'newuser@test.edu'
    assert data['role'] == 'faculty'
    assert data['is_active'] is True
    assert 'password' not in data
    assert 'hashed_password' not in data


def test_register_duplicate_email(client):
    # First registration
    payload = {
        'email': 'duplicate@test.edu',
        'password': 'password123',
        'role': 'admin',
        'tenant_id': 1,
    }
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 200

    # Second registration with same email should fail
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 400
    assert 'already registered' in response.json()['detail'].lower()


def test_login_success(client):
    response = client.post(
        '/auth/login',
        data={'username': 'test@test.edu', 'password': 'testpassword123'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_login_wrong_password(client):
    response = client.post(
        '/auth/login',
        data={'username': 'test@test.edu', 'password': 'wrongpassword'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    response = client.get('/auth/me', headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'test@test.edu'
    assert data['role'] == 'admin'


def test_protected_route_requires_auth(client):
    response = client.get('/auth/me')
    assert response.status_code == 401
