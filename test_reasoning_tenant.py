"""
English: Verify the reasoning loop now passes tenant thresholds to the LLM prompt.
Roman Urdu: Verify karo reasoning loop ab tenant thresholds LLM prompt mein bhejta hai.
"""
import json
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.core.reasoning import reason

db = SessionLocal()
try:
    t = db.query(Tenant).first()
    settings = json.loads(t.settings_json)
    print(f"Tenant threshold: {settings.get('attendance_threshold')}")

    r = reason(
        "show me students with low attendance",
        user_id=1, user_email="admin@demo.university.edu", tenant_id=t.id,
    )
    print(f"Iterations: {r.get('iterations')}")
    for tc in r.get('tool_calls', []):
        print(f"  Tool: {tc['tool']}, args: {tc['args']}, results: {tc['summary'].get('count')}")
    print(f"Answer preview: {r.get('answer', '')[:200]}")
finally:
    db.close()
