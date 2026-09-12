import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.core.database import Base, get_db
from backend.app.models.tenant import Tenant
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

# In-memory SQLite database for tests — isolated from real data
engine = create_engine(
    'sqlite://',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='function')
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def client(db_session):
    # Seed a test tenant and admin user
    tenant = Tenant(name='Test University', domain='test.edu')
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)

    user = User(
        tenant_id=tenant.id,
        email='test@test.edu',
        hashed_password=get_password_hash('testpassword123'),
        role='admin',
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    response = client.post(
        '/auth/login',
        data={'username': 'test@test.edu', 'password': 'testpassword123'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    assert response.status_code == 200, response.text
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}
