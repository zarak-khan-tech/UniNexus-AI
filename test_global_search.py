"""
English: Verify global search returns grouped results.
Roman Urdu: Global search grouped results return kare verify karo.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).filter(User.role == 'admin').first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
db.close()
h = {'Authorization': 'Bearer ' + token}

for q in ['ali', 'exam', 'attendance', 'CS10']:
    r = requests.get(f'http://127.0.0.1:8000/search?q={q}', headers=h)
    print(f"--- Query: '{q}' → Status {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        for cat in ('students', 'courses', 'documents', 'agents', 'tools'):
            count = len(data.get(cat, []))
            if count:
                print(f"  {cat}: {count}")
    print()
