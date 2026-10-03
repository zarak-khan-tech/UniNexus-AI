"""
English: Verify agent definitions API and DB-driven listing.
Roman Urdu: Agent definitions API aur DB-driven listing verify karo.
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

h = {'Authorization': 'Bearer ' + token}

print("=" * 60)
print("Test 1: GET /agents/list (should read from DB)")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/agents/list', headers=h)
print(json.dumps(r.json(), indent=2))

print()
print("=" * 60)
print("Test 2: PATCH description")
print("=" * 60)
r = requests.patch(
    'http://127.0.0.1:8000/agents/definitions/RiskAgent',
    headers={**h, 'Content-Type': 'application/json'},
    data=json.dumps({'description': 'Updated description: analyzes risk from attendance + grades.'}),
)
print(json.dumps(r.json(), indent=2))

print()
print("=" * 60)
print("Test 3: Disable AttendanceAgent, then verify it's gone")
print("=" * 60)
r = requests.patch(
    'http://127.0.0.1:8000/agents/definitions/AttendanceAgent',
    headers={**h, 'Content-Type': 'application/json'},
    data=json.dumps({'is_active': False}),
)
print("Disabled:", r.json().get('definition', {}).get('is_active'))

r = requests.get('http://127.0.0.1:8000/agents/list', headers=h)
names = [a['name'] for a in r.json()['agents']]
print("Active agents now:", names)

# Restore
r = requests.patch(
    'http://127.0.0.1:8000/agents/definitions/AttendanceAgent',
    headers={**h, 'Content-Type': 'application/json'},
    data=json.dumps({'is_active': True}),
)
print("Restored AttendanceAgent")
