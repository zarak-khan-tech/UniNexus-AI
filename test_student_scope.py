"""
English: Verify student sees only own data; admin sees all.
Roman Urdu: Verify karo student sirf apna data dekhta hai; admin sab dekhta hai.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.models.tenant import Tenant
from backend.app.core.security import create_access_token, get_password_hash

db = SessionLocal()
try:
    t = db.query(Tenant).first()

    # English: Create a "student" user whose email matches an actual Student row,
    #          so the email-matching logic has a real record to return.
    # Roman Urdu: Ek "student" user banao jiska email ek actual Student row se
    #             match kare taake email-matching logic kaam kare.
    target_student = db.query(Student).filter(Student.tenant_id == t.id).first()
    print(f"Target student: {target_student.first_name} {target_student.last_name} ({target_student.email})")

    student_user_email = target_student.email
    existing = db.query(User).filter(User.email == student_user_email).first()
    if not existing:
        existing = User(
            tenant_id=t.id, email=student_user_email,
            hashed_password=get_password_hash('studentpass123'),
            role='student', is_active=True,
        )
        db.add(existing)
        db.commit()
        db.refresh(existing)
        print(f"Created student user for: {student_user_email}")

    admin = db.query(User).filter(User.role == 'admin').first()
    student_user = existing

    admin_token = create_access_token(data={'sub': admin.email, 'role': admin.role, 'tenant_id': admin.tenant_id})
    student_token = create_access_token(data={'sub': student_user.email, 'role': student_user.role, 'tenant_id': student_user.tenant_id})
finally:
    db.close()

h_admin = {'Authorization': 'Bearer ' + admin_token}
h_student = {'Authorization': 'Bearer ' + student_token}

print()
print("=" * 60)
print("Test 1: Admin GET /academic/students")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/academic/students', headers=h_admin)
data = r.json()
print(f"Scope: {data.get('scope')}, Total: {data.get('total')}")

print()
print("=" * 60)
print("Test 2: Student GET /academic/students")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/academic/students', headers=h_student)
data = r.json()
print(f"Scope: {data.get('scope')}, Total: {data.get('total')}")
for s in data.get('students', []):
    print(f"  - {s['first_name']} {s['last_name']} ({s['email']})")

print()
print("=" * 60)
print("Test 3: Admin GET /academic/courses")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/academic/courses', headers=h_admin)
data = r.json()
print(f"Scope: {data.get('scope')}, Total: {data.get('total')}")

print()
print("=" * 60)
print("Test 4: Student GET /academic/courses")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/academic/courses', headers=h_student)
data = r.json()
print(f"Scope: {data.get('scope')}, Total: {data.get('total')}")
for c in data.get('courses', []):
    print(f"  - {c['course_code']}: {c['title']}")
