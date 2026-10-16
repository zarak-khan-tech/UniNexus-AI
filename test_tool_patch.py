"""
English: Verify tool PATCH + toggle works.
Roman Urdu: Tool PATCH + toggle verify karo.
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
print("Test 1: Disable semantic_search")
print("=" * 60)
r = requests.patch(
    'http://127.0.0.1:8000/tools/definitions/semantic_search',
    headers={**h, 'Content-Type': 'application/json'},
    data=json.dumps({'is_active': False}),
)
print(f"Status: {r.status_code}")
print(f"is_active: {r.json().get('definition', {}).get('is_active')}")

print()
print("=" * 60)
print("Test 2: GET /tools shows paused")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/tools', headers=h)
for t in r.json().get('tools', []):
    if t['name'] == 'semantic_search':
        print(f"semantic_search is_active: {t.get('is_active')}")

# Restore
print()
print("=" * 60)
print("Restoring")
print("=" * 60)
requests.patch(
    'http://127.0.0.1:8000/tools/definitions/semantic_search',
    headers={**h, 'Content-Type': 'application/json'},
    data=json.dumps({'is_active': True}),
)
print("Restored")
