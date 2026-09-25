"""
English: Tests the exact production orchestrator path to see why planning falls back.
Roman Urdu: Production orchestrator ka exact path test karta hai taake pata chale fallback kyun ho raha hai.
"""
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# English: Register agents exactly like the API does.
# Roman Urdu: Agents register karo bilkul jaise API karta hai.
from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent
from backend.app.agents.orchestrator import OrchestratorAgent

registry.register(AttendanceAgent())
registry.register(PolicyAgent())
registry.register(RiskAgent())
registry.register(KnowledgeAgent())

print("=" * 60)
print("Running orchestrator exactly like /agents/run")
print("=" * 60)

orch = OrchestratorAgent()
result = orch.execute({"request": "Show me students with attendance risk"})

print()
print("=" * 60)
print("RESULT:")
print("=" * 60)
print("Planning source:", result.get("planning_source"))
print("Status:", result.get("status"))
print()
print("Plan:")
for step in result.get("execution_plan", []):
    print(f"  Step {step.get('step')}: {step.get('agent')} -> {step.get('action')}")
