"""
English: Verify tenant threshold is used when no percentage is in the request.
Roman Urdu: Verify karo tenant threshold use hota hai jab request mein percentage na ho.
"""
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent
import json

# Register agent
registry.register(AttendanceAgent())

db = SessionLocal()
try:
    t = db.query(Tenant).first()
    settings = json.loads(t.settings_json)
    print(f"Current attendance_threshold in settings: {settings.get('attendance_threshold')}")

    # Test 1: default settings
    agent = registry.get_agent('AttendanceAgent')
    r = agent.execute({'request': 'show me students with low attendance', 'tenant_id': t.id})
    print(f"Test 1 - threshold: {r.get('threshold')}, source: {r.get('threshold_source')}, flagged: {r.get('total_flagged')}")

    # Test 2: override tenant setting to 85 and re-run
    settings['attendance_threshold'] = 85
    t.settings_json = json.dumps(settings)
    db.commit()

    r2 = agent.execute({'request': 'show me students with low attendance', 'tenant_id': t.id})
    print(f"Test 2 - threshold: {r2.get('threshold')}, source: {r2.get('threshold_source')}, flagged: {r2.get('total_flagged')}")

    # Test 3: request override
    r3 = agent.execute({'request': 'show me students with attendance below 60%', 'tenant_id': t.id})
    print(f"Test 3 - threshold: {r3.get('threshold')}, source: {r3.get('threshold_source')}, flagged: {r3.get('total_flagged')}")

    # Restore
    settings['attendance_threshold'] = 75
    t.settings_json = json.dumps(settings)
    db.commit()
    print("Restored threshold to 75")
finally:
    db.close()
