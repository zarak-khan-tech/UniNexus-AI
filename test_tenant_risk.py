"""
English: Verify RiskAgent uses tenant-configured thresholds.
Roman Urdu: Verify karo RiskAgent tenant-configured thresholds use karta hai.
"""
import json
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.agents.registry import registry
from backend.app.agents.specialized import RiskAgent

registry.register(RiskAgent())

db = SessionLocal()
try:
    t = db.query(Tenant).first()
    settings = json.loads(t.settings_json)
    print(f"Current risk_high={settings.get('risk_high_threshold')}, "
          f"risk_medium={settings.get('risk_medium_threshold')}")

    agent = registry.get_agent('RiskAgent')

    # Test 1: default settings
    r1 = agent.execute({'request': 'who is at risk', 'tenant_id': t.id})
    print(f"Test 1 - thresholds: {r1.get('thresholds')}, at_risk: {len(r1.get('at_risk_students', []))}")

    # Test 2: tighten medium threshold to 85
    settings['risk_medium_threshold'] = 85
    t.settings_json = json.dumps(settings)
    db.commit()

    r2 = agent.execute({'request': 'who is at risk', 'tenant_id': t.id})
    print(f"Test 2 - thresholds: {r2.get('thresholds')}, at_risk: {len(r2.get('at_risk_students', []))}")

    # Restore
    settings['risk_medium_threshold'] = 75
    t.settings_json = json.dumps(settings)
    db.commit()
    print("Restored threshold to 75")
finally:
    db.close()
