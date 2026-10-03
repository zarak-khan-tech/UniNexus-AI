"""
English: Test course + enrollment import in one go.
Roman Urdu: Course + enrollment import ko ek saath test karo.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.course import Course
from backend.app.models.enrollment import Enrollment
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).filter(User.role == 'admin').first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
db.close()

h = {'Authorization': 'Bearer ' + token}

# ============ Courses ============
print("=" * 60)
print("TEST 1: Import courses")
print("=" * 60)
courses_csv = """course_code,title,credit_hours,department
CS401,Advanced Algorithms,4,Computer Science
CS402,Machine Learning,4,Computer Science
MATH301,Discrete Mathematics,3,Mathematics
CS401,Duplicate,4,Computer Science
BADCODE,Bad Hours,15,Physics
"""
r = requests.post(
    'http://127.0.0.1:8000/import/courses',
    headers=h,
    files={'file': ('courses.csv', courses_csv, 'text/csv')},
)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# ============ Enrollments ============
print()
print("=" * 60)
print("TEST 2: Import enrollments (existing students into existing courses)")
print("=" * 60)
# Ali Khan S101 was pre-existing; use those courses that exist
enroll_csv = """student_number,course_code,grade,attendance_percentage
S101,CS401,A,85
S101,CS402,B+,78
S102,CS401,B,90
S101,CS401,A,90
S999,CS401,A,85
S101,NOTREAL,A,85
S101,MATH301,C,150
"""
r = requests.post(
    'http://127.0.0.1:8000/import/enrollments',
    headers=h,
    files={'file': ('enrollments.csv', enroll_csv, 'text/csv')},
)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# ============ Verify DB ============
print()
print("=" * 60)
print("VERIFY: New data in DB")
print("=" * 60)
db = SessionLocal()
new_courses = db.query(Course).filter(Course.course_code.in_(['CS401', 'CS402', 'MATH301'])).count()
print(f"New courses in DB: {new_courses}  (expected: 3)")
# English: Enrollment for S101 in CS401 should exist once.
s101_cs401 = db.query(Enrollment).join(Course, Enrollment.course_id == Course.id).filter(
    Course.course_code == 'CS401'
).count()
print(f"CS401 enrollments: {s101_cs401}")
db.close()
