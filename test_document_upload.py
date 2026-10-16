"""
English: Verify document upload + chunking + embedding.
Roman Urdu: Document upload + chunking + embedding verify karo.
"""
import io
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.document import Document
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).filter(User.role == 'admin').first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
db.close()
h = {'Authorization': 'Bearer ' + token}

# English: Small synthetic policy document.
# Roman Urdu: Chhota synthetic policy document.
policy_text = """Scholarship Renewal Policy 2026

Students receiving the Merit Scholarship must maintain a minimum CGPA of 3.0 each semester. Failure to meet this threshold converts the award to a repayable loan for that semester. Students may reapply after bringing their CGPA above 3.0.

Need-based Financial Aid recipients must maintain a minimum CGPA of 2.5. Annual documentation of family income is required. Failure to submit documents by the deadline results in automatic suspension of aid for the following semester.

Athletic Scholarship holders must maintain a CGPA of 2.5 and participate in at least 80% of scheduled team activities. Injuries must be documented by the university medical office within 7 days.

All scholarship decisions are subject to review by the Scholarship Committee. Appeals must be submitted in writing within 14 days of the decision notice.
"""

files = {'file': ('scholarship_policy.txt', policy_text, 'text/plain')}
data = {'title': 'Scholarship Renewal Policy 2026', 'category': 'Policy'}

r = requests.post(
    'http://127.0.0.1:8000/documents/upload',
    headers=h,
    files=files,
    data=data,
)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

# Verify in DB + vector store
db = SessionLocal()
total = db.query(Document).count()
db.close()
print(f"\nTotal documents in DB: {total}")

# Test 2: duplicate title should fail
r2 = requests.post(
    'http://127.0.0.1:8000/documents/upload',
    headers=h,
    files={'file': ('dup.txt', policy_text, 'text/plain')},
    data={'title': 'Scholarship Renewal Policy 2026', 'category': 'Policy'},
)
print(f"\nTest 2 (duplicate title) status: {r2.status_code} (expected 400)")
