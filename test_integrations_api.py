"""
English: Verify GET /integrations returns registered adapters with honest status.
Roman Urdu: GET /integrations registered adapters honest status ke saath return kare verify karo.
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

print("=" * 60)
print("GET /integrations")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/integrations', headers=h)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))

print()
print("=" * 60)
print("POST /integrations/generic_rest/test (honest failure expected)")
print("=" * 60)
r = requests.post('http://127.0.0.1:8000/integrations/generic_rest/test', headers=h)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))
