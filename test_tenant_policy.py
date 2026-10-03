"""
English: Verify PolicyAgent reads threshold from tenant settings.
Roman Urdu: Verify karo PolicyAgent tenant settings se threshold padhta hai.
"""
import json
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.agents.registry import registry
from backend.app.agents.specialized import PolicyAgent

registry.register(PolicyAgent())

db = SessionLocal()
try:
    t = db.query(Tenant).first()
    settings = json.loads(t.settings_json)
    print(f"Current attendance_threshold: {settings.get('attendance_threshold')}")

    agent = registry.get_agent('PolicyAgent')

    # Test 1: default
    r1 = agent.execute({'request': 'what is the attendance policy', 'tenant_id': t.id})
    print(f"Test 1 - threshold: {r1.get('policy_threshold')}, rule: {r1.get('rule')}")

    # Test 2: change setting
    settings['attendance_threshold'] = 80
    t.settings_json = json.dumps(settings)
    db.commit()

    r2 = agent.execute({'request': 'what is the attendance policy', 'tenant_id': t.id})
    print(f"Test 2 - threshold: {r2.get('policy_threshold')}, rule: {r2.get('rule')}")

    # Restore
    settings['attendance_threshold'] = 75
    t.settings_json = json.dumps(settings)
    db.commit()
    print("Restored threshold to 75")
finally:
    db.close()
