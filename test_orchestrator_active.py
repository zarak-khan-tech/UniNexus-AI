"""
English: Verify orchestrator skips disabled agents.
Roman Urdu: Orchestrator disabled agents skip karta hai ye verify karo.
"""
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.services.agent_definitions import update_agent_definition
from backend.app.agents.registry import registry
from backend.app.agents.orchestrator import OrchestratorAgent
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent

registry.register(AttendanceAgent())
registry.register(PolicyAgent())
registry.register(RiskAgent())
registry.register(KnowledgeAgent())

db = SessionLocal()
t = db.query(Tenant).first()
tenant_id = t.id
db.close()

orch = OrchestratorAgent()

print("=" * 60)
print("Test 1: All agents active")
print("=" * 60)
r = orch.execute({'request': 'show me students with attendance risk', 'tenant_id': tenant_id})
print(f"Planning source: {r.get('planning_source')}")
print(f"Plan: {[s['agent'] for s in r.get('execution_plan', [])]}")
print(f"Executed steps: {len(r.get('execution_results', []))}")

print()
print("=" * 60)
print("Test 2: Disable RiskAgent")
print("=" * 60)
update_agent_definition(tenant_id, 'RiskAgent', {'is_active': False})
r = orch.execute({'request': 'show me students with attendance risk', 'tenant_id': tenant_id})
print(f"Planning source: {r.get('planning_source')}")
print(f"Plan: {[s['agent'] for s in r.get('execution_plan', [])]}")
for step in r.get('execution_results', []):
    if step.get('error'):
        print(f"  Step {step['step']} ({step['agent']}): ERROR - {step['error']}")

print()
print("=" * 60)
print("Test 3: Restore RiskAgent, disable AttendanceAgent")
print("=" * 60)
update_agent_definition(tenant_id, 'RiskAgent', {'is_active': True})
update_agent_definition(tenant_id, 'AttendanceAgent', {'is_active': False})
r = orch.execute({'request': 'show me students with low attendance', 'tenant_id': tenant_id})
print(f"Plan: {[s['agent'] for s in r.get('execution_plan', [])]}")

# Restore all
update_agent_definition(tenant_id, 'AttendanceAgent', {'is_active': True})
update_agent_definition(tenant_id, 'RiskAgent', {'is_active': True})
print()
print("All agents restored to active")
