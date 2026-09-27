from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent
from backend.app.agents.orchestrator import OrchestratorAgent

registry.register(AttendanceAgent())
registry.register(PolicyAgent())
registry.register(RiskAgent())
registry.register(KnowledgeAgent())

orch = OrchestratorAgent()
result = orch.execute({'request': 'Show me students with attendance risk'})

print('=' * 60)
print('PLANNING SOURCE:', result.get('planning_source'))
print('MODE:', result.get('mode'))
print('=' * 60)

for step in result.get('execution_results', []):
    r = step.get('result', {})
    print(f"Step {step['step']}: {step['agent']}")
    print(f"  Tool used: {r.get('tool_used', 'none')}")
    if step['agent'] == 'AttendanceAgent':
        print(f"  Flagged: {r.get('total_flagged', 0)} students")
    elif step['agent'] == 'RiskAgent':
        print(f"  At risk: {len(r.get('at_risk_students', []))} enrollments")
