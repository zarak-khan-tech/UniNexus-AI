"""
English: Verify the execution detail endpoint returns full data.
Roman Urdu: Execution detail endpoint poori data return kare verify karo.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.agent_execution import AgentExecution
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).filter(User.role == 'admin').first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
# Find any execution for this tenant
row = db.query(AgentExecution).filter(AgentExecution.tenant_id == u.tenant_id).order_by(
    AgentExecution.created_at.desc()).first()
exec_id = row.id if row else None
db.close()

if not exec_id:
    print("No executions in DB — run a task first")
else:
    h = {'Authorization': 'Bearer ' + token}
    r = requests.get(f'http://127.0.0.1:8000/agents/executions/{exec_id}', headers=h)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"ID: {data.get('id')}")
    print(f"Request: {data.get('original_request')}")
    print(f"Status: {data.get('status')}")
    print(f"Duration: {data.get('duration_ms')} ms")
    print(f"Plan steps: {len(data.get('execution_plan') or [])}")
