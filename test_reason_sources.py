"""
English: Verify sources are returned for a policy query.
Roman Urdu: Policy query ke liye sources return hote hain ye verify karo.
"""
import json
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.core.reasoning import reason

db = SessionLocal()
t = db.query(Tenant).first()
tid = t.id
db.close()

r = reason(
    "what happens if I fail an exam?",
    user_id=1, user_email="admin@demo.university.edu", tenant_id=tid,
)
print("Iterations:", r.get('iterations'))
print("Tool calls:", len(r.get('tool_calls', [])))
print()
print("SOURCES RETURNED:")
for s in r.get('sources', []):
    print(f"  - {s['title']} ({s['category']}) similarity={s['similarity']}")
print()
print("Answer preview:", r.get('answer', '')[:200])
