"""
English: Verify tool definitions are DB-driven and API returns them.
Roman Urdu: Tool definitions DB-driven hain aur API return karta hai — verify.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.tool_definition import ToolDefinition
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).filter(User.role == 'admin').first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
total_db = db.query(ToolDefinition).count()
db.close()

h = {'Authorization': 'Bearer ' + token}

print(f"ToolDefinition rows in DB: {total_db}")
print()
print("=" * 60)
print("GET /tools response")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/tools', headers=h)
data = r.json()
print(f"Counts: {json.dumps(data.get('counts'), indent=2)}")
print(f"Tools returned: {len(data.get('tools', []))}")
for t in data.get('tools', []):
    print(f"  - {t['name']:30} [{t['permission']:11}] v{t.get('version','?')} active={t.get('is_active')}")
