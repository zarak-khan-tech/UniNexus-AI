"""
English: Verify RBAC — admin works, student gets 403.
Roman Urdu: RBAC verify karo — admin chalta hai, student 403 paata hai.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.tenant import Tenant
from backend.app.core.security import create_access_token, get_password_hash

db = SessionLocal()
try:
    # Ensure a student user exists for testing
    t = db.query(Tenant).first()
    student_email = 'student.rbac@demo.university.edu'
    existing = db.query(User).filter(User.email == student_email).first()
    if not existing:
        existing = User(
            tenant_id=t.id, email=student_email,
            hashed_password=get_password_hash('studentpass123'),
            role='student', is_active=True,
        )
        db.add(existing)
        db.commit()
        db.refresh(existing)
        print(f"Created student user: {student_email}")

    admin = db.query(User).filter(User.role == 'admin').first()
    student = existing

    admin_token = create_access_token(data={'sub': admin.email, 'role': admin.role, 'tenant_id': admin.tenant_id})
    student_token = create_access_token(data={'sub': student.email, 'role': student.role, 'tenant_id': student.tenant_id})
finally:
    db.close()

print()
print("=" * 60)
print("Test 1: Student tries PATCH agent definition → expect 403")
print("=" * 60)
r = requests.patch(
    'http://127.0.0.1:8000/agents/definitions/RiskAgent',
    headers={'Authorization': 'Bearer ' + student_token, 'Content-Type': 'application/json'},
    data=json.dumps({'description': 'Hacked by student'}),
)
print(f"Status: {r.status_code}")
print(f"Detail: {r.json().get('detail')}")

print()
print("=" * 60)
print("Test 2: Admin PATCH agent definition → expect 200")
print("=" * 60)
r = requests.patch(
    'http://127.0.0.1:8000/agents/definitions/RiskAgent',
    headers={'Authorization': 'Bearer ' + admin_token, 'Content-Type': 'application/json'},
    data=json.dumps({'description': 'Analyzes academic risk via the list_enrollments tool.'}),
)
print(f"Status: {r.status_code}")
print(f"ok: {r.json().get('ok')}")

print()
print("=" * 60)
print("Test 3: Student tries PUT tenant settings → expect 403")
print("=" * 60)
r = requests.put(
    'http://127.0.0.1:8000/tenant/settings',
    headers={'Authorization': 'Bearer ' + student_token, 'Content-Type': 'application/json'},
    data=json.dumps({'settings': {'attendance_threshold': 10}}),
)
print(f"Status: {r.status_code}")
print(f"Detail: {r.json().get('detail')}")

print()
print("=" * 60)
print("Test 4: Admin PUT tenant settings → expect 200")
print("=" * 60)
r = requests.put(
    'http://127.0.0.1:8000/tenant/settings',
    headers={'Authorization': 'Bearer ' + admin_token, 'Content-Type': 'application/json'},
    data=json.dumps({'settings': {'attendance_threshold': 75}}),
)
print(f"Status: {r.status_code}")
print(f"ok: {r.json().get('ok')}")
