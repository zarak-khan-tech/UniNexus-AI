from backend.app.core.llm_gateway import get_gateway

gw = get_gateway()
prompt = """You plan tasks for a university AI system.

Agents: AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent.

User question: "Show me students with attendance risk"

Return JSON with a "plan" field. Example: {"plan": [{"step": 1, "agent": "AttendanceAgent", "action": "fetch data"}]}

Respond with JSON only."""

print("Testing Gemini via gateway...")
print("=" * 60)
resp = gw.generate(prompt, json_mode=True)
print("Provider:", resp.provider)
print("Model:", resp.model)
print("Success:", resp.success)
print("Error:", resp.error)
print("-" * 60)
print("Raw text (first 500 chars):")
print(resp.text[:500] if resp.text else "(empty)")
