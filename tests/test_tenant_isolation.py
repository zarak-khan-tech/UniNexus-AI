"""
English: Multi-tenant isolation tests — prove one tenant cannot access 
another tenant's protected data.
Roman Urdu: Multi-tenant isolation tests — prove karo ek tenant doosre 
tenant ka protected data access nahi kar sakta.
"""
import pytest
from backend.app.models.tenant import Tenant
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.document import Document
from backend.app.models.notification import Notification
from backend.app.models.agent_execution import AgentExecution
from backend.app.models.user import User
from backend.app.core.security import get_password_hash


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _create_second_tenant(db_session, name='Other University', domain='other.edu',
                          admin_email='admin2@other.edu'):
    """English: Create a fresh tenant + admin user for isolation tests.
    Roman Urdu: Isolation tests ke liye nayi tenant + admin user banao."""
    t = Tenant(name=name, domain=domain)
    db_session.add(t)
    db_session.commit()
    db_session.refresh(t)

    u = User(
        tenant_id=t.id,
        email=admin_email,
        hashed_password=get_password_hash('pass123456'),
        role='admin',
        is_active=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return t, u


def _login(client, email, password='pass123456'):
    """English: Log in a user and return auth headers.
    Roman Urdu: User ko login karo aur auth headers return karo."""
    r = client.post(
        '/auth/login',
        data={'username': email, 'password': password},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    assert r.status_code == 200, r.text
    return {'Authorization': 'Bearer ' + r.json()['access_token']}


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

def test_students_are_isolated(client, db_session, auth_headers):
    """
    English: Tenant A's admin must not see Tenant B's students.
    Roman Urdu: Tenant A ka admin Tenant B ke students nahi dekh sakta.
    """
    t2, _ = _create_second_tenant(db_session)

    s_a = Student(tenant_id=1, student_number='A1', first_name='Alice',
                  last_name='Alpha', email='alice@test.edu', enrollment_year=2024)
    s_b = Student(tenant_id=t2.id, student_number='B1', first_name='Bob',
                  last_name='Beta', email='bob@other.edu', enrollment_year=2024)
    db_session.add_all([s_a, s_b])
    db_session.commit()

    r = client.get('/academic/students', headers=auth_headers)
    assert r.status_code == 200
    numbers = [s['student_number'] for s in r.json()['students']]
    assert 'A1' in numbers
    assert 'B1' not in numbers


def test_courses_are_isolated(client, db_session, auth_headers):
    """
    English: Tenant A's admin must not see Tenant B's courses.
    Roman Urdu: Tenant A ka admin Tenant B ke courses nahi dekh sakta.
    """
    t2, _ = _create_second_tenant(db_session)

    c_a = Course(tenant_id=1, course_code='CSA1', title='Course A',
                 credit_hours=3, department='CS')
    c_b = Course(tenant_id=t2.id, course_code='CSB1', title='Course B',
                 credit_hours=3, department='CS')
    db_session.add_all([c_a, c_b])
    db_session.commit()

    r = client.get('/academic/courses', headers=auth_headers)
    assert r.status_code == 200
    codes = [c['course_code'] for c in r.json()['courses']]
    assert 'CSA1' in codes
    assert 'CSB1' not in codes


def test_documents_are_isolated(client, db_session, auth_headers):
    """
    English: Tenant A's admin must not see Tenant B's documents.
    Roman Urdu: Tenant A ka admin Tenant B ke documents nahi dekh sakta.
    """
    t2, _ = _create_second_tenant(db_session)

    d_a = Document(tenant_id=1, title='Doc A', category='Policy', content='A content')
    d_b = Document(tenant_id=t2.id, title='Doc B', category='Policy', content='B content')
    db_session.add_all([d_a, d_b])
    db_session.commit()

    r = client.get('/academic/documents', headers=auth_headers)
    assert r.status_code == 200
    titles = [d['title'] for d in r.json()['documents']]
    assert 'Doc A' in titles
    assert 'Doc B' not in titles


def test_notifications_are_isolated(client, db_session, auth_headers):
    """
    English: Tenant A's admin must not see Tenant B's notifications.
    Roman Urdu: Tenant A ka admin Tenant B ki notifications nahi dekh sakta.
    """
    t2, u2 = _create_second_tenant(db_session)

    n_a = Notification(tenant_id=1, user_id=1, kind='system', title='Notif A', body='A')
    n_b = Notification(tenant_id=t2.id, user_id=u2.id, kind='system', title='Notif B', body='B')
    db_session.add_all([n_a, n_b])
    db_session.commit()

    r = client.get('/notifications', headers=auth_headers)
    assert r.status_code == 200
    titles = [n['title'] for n in r.json()['notifications']]
    assert 'Notif A' in titles
    assert 'Notif B' not in titles


def test_agent_executions_are_isolated(client, db_session, auth_headers):
    """
    English: Tenant A's admin must not see Tenant B's execution history.
    Roman Urdu: Tenant A ka admin Tenant B ka execution history nahi dekh sakta.
    """
    t2, u2 = _create_second_tenant(db_session)

    e_a = AgentExecution(
        tenant_id=1, user_id=1, user_email='test@test.edu',
        original_request='A request', status='completed',
        execution_plan_json='[]', execution_results_json='[]',
    )
    e_b = AgentExecution(
        tenant_id=t2.id, user_id=u2.id, user_email=u2.email,
        original_request='B request', status='completed',
        execution_plan_json='[]', execution_results_json='[]',
    )
    db_session.add_all([e_a, e_b])
    db_session.commit()

    r = client.get('/agents/executions', headers=auth_headers)
    assert r.status_code == 200
    requests = [e['original_request'] for e in r.json()['executions']]
    assert 'A request' in requests
    assert 'B request' not in requests


def test_tenant_b_admin_cannot_see_tenant_a_via_login(client, db_session):
    """
    English: Log in as Tenant B's admin and confirm they don't see Tenant A's data.
    Roman Urdu: Tenant B ke admin se login karo aur confirm karo ke wo Tenant A ka 
    data nahi dekhte.
    """
    t2, _ = _create_second_tenant(db_session)

    s_a = Student(tenant_id=1, student_number='A1', first_name='Alice',
                  last_name='Alpha', email='alice@test.edu', enrollment_year=2024)
    s_b = Student(tenant_id=t2.id, student_number='B1', first_name='Bob',
                  last_name='Beta', email='bob@other.edu', enrollment_year=2024)
    db_session.add_all([s_a, s_b])
    db_session.commit()

    h_b = _login(client, 'admin2@other.edu')
    r = client.get('/academic/students', headers=h_b)
    assert r.status_code == 200
    numbers = [s['student_number'] for s in r.json()['students']]
    assert 'B1' in numbers
    assert 'A1' not in numbers


def test_tenant_settings_are_isolated(client, db_session, auth_headers):
    """
    English: Tenant A's admin can only read Tenant A's settings.
    Roman Urdu: Tenant A ka admin sirf Tenant A ki settings padh sakta hai.
    """
    t2, _ = _create_second_tenant(db_session)

    import json
    t2.settings_json = json.dumps({'university_name': 'Tenant B University'})
    db_session.commit()

    r = client.get('/tenant/settings', headers=auth_headers)
    assert r.status_code == 200
    assert r.json()['tenant_id'] == 1
    assert r.json()['settings'].get('university_name') != 'Tenant B University'


def test_admin_of_tenant_b_creates_student_in_own_tenant(client, db_session):
    """
    English: When Tenant B's admin imports a student, it lands in Tenant B — 
    not Tenant A.
    Roman Urdu: Jab Tenant B ka admin student import kare, wo Tenant B mein 
    jaye — Tenant A mein nahi.
    """
    t2, u2 = _create_second_tenant(db_session, name='Third University', 
                                   domain='third.edu', admin_email='admin3@third.edu')
    h_b = _login(client, 'admin3@third.edu')

    csv_content = (
        "student_number,first_name,last_name,email,enrollment_year\n"
        "S999,Charlie,Gamma,charlie@third.edu,2024\n"
    )
    r = client.post(
        '/import/students',
        headers=h_b,
        files={'file': ('students.csv', csv_content, 'text/csv')},
    )
    assert r.status_code == 200, r.text
    assert r.json()['added'] == 1

    new_student = db_session.query(Student).filter(Student.student_number == 'S999').first()
    assert new_student is not None
    assert new_student.tenant_id == t2.id
