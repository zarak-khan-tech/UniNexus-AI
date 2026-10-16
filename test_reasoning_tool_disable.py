"""
English: Verify reasoning loop skips disabled tools.
Roman Urdu: Verify karo reasoning loop disabled tools skip karta hai.
"""
import json
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.services.tool_definitions import update_tool_definition
from backend.app.core.reasoning import reason

db = SessionLocal()
t = db.query(Tenant).first()
tid = t.id
db.close()

print("=" * 60)
print("Test 1: All tools active — baseline")
print("=" * 60)
r = reason(
    "what happens if I fail an exam?",
    user_id=1, user_email="admin@demo.university.edu", tenant_id=tid,
)
print(f"Iterations: {r.get('iterations')}")
print(f"Tool calls: {[tc['tool'] for tc in r.get('tool_calls', [])]}")
print(f"Sources: {[s['title'] for s in r.get('sources', [])]}")
print()

print("=" * 60)
print("Test 2: Disable semantic_search — reasoning should not call it")
print("=" * 60)
update_tool_definition(tid, 'semantic_search', {'is_active': False})
r2 = reason(
    "what happens if I fail an exam?",
    user_id=1, user_email="admin@demo.university.edu", tenant_id=tid,
)
print(f"Iterations: {r2.get('iterations')}")
tools_called = [tc['tool'] for tc in r2.get('tool_calls', [])]
print(f"Tool calls: {tools_called}")
print(f"Answer preview: {r2.get('answer', '')[:200]}")
assert 'semantic_search' not in tools_called, "semantic_search was called even though disabled!"
print("PASS: semantic_search was NOT called")
print()

print("=" * 60)
print("Restore semantic_search")
print("=" * 60)
update_tool_definition(tid, 'semantic_search', {'is_active': True})
print("Restored")
