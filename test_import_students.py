"""
English: Test CSV student import — upload a small CSV with 3 valid, 1 duplicate, 1 invalid row.
Roman Urdu: CSV student import test — 3 valid, 1 duplicate, 1 invalid row wali CSV upload karo.
"""
import io
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).filter(User.role == 'admin').first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
db.close()

csv_content = """student_number,first_name,last_name,email,enrollment_year
S201,Imported,One,imported.one@demo.edu,2024
S202,Imported,Two,imported.two@demo.edu,2023
S203,Imported,Three,imported.three@demo.edu,2024
S101,Duplicate,Ali,ali@demo.edu,2024
S204,Bad,Email,not-an-email,2024
S205,Imported,Four,imported.four@demo.edu,abc
"""

files = {'file': ('students.csv', csv_content, 'text/csv')}
r = requests.post(
    'http://127.0.0.1:8000/import/students',
    headers={'Authorization': 'Bearer ' + token},
    files=files,
)

print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# English: Confirm only 3 new students landed.
from backend.app.models.student import Student
db = SessionLocal()
total_new = db.query(Student).filter(Student.student_number.in_(['S201', 'S202', 'S203', 'S204', 'S205'])).count()
print(f"\nNew imported students in DB: {total_new}  (expected: 3)")
db.close()
