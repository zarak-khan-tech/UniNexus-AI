"""
English: Verify tenant settings endpoint returns backfilled defaults.
Roman Urdu: Verify karo tenant settings endpoint defaults return karta hai.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
db.close()

r = requests.get(
    'http://127.0.0.1:8000/tenant/settings',
    headers={'Authorization': 'Bearer ' + token},
)
print(json.dumps(r.json(), indent=2))
