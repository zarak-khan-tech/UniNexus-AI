"""
English: Verify per-agent health endpoint.
Roman Urdu: Per-agent health endpoint verify karo.
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

r = requests.get('http://127.0.0.1:8000/agents/health', headers=h)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))
