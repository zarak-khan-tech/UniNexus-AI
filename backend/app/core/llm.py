import json
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Use the bigger 3B model — much smarter than the 1B version
DEFAULT_MODEL = 'llama3.2:latest'

def check_ollama_status() -> Dict[str, Any]:
    if not OLLAMA_AVAILABLE:
        return {'available': False, 'reason': 'ollama python package not installed'}
    try:
        models_response = ollama.list()
        raw_models = models_response.get('models', []) if isinstance(models_response, dict) else getattr(models_response, 'models', [])
        model_names = []
        for m in raw_models:
            name = m.get('name') if isinstance(m, dict) else getattr(m, 'model', None)
            if name:
                model_names.append(name)
        # Check for either version of llama3.2
        model_ready = any('llama3.2' in (n or '') for n in model_names)
        return {
            'available': True,
            'default_model': DEFAULT_MODEL,
            'model_ready': model_ready,
            'installed_models': model_names,
        }
    except Exception as e:
        return {'available': False, 'reason': str(e)}

def plan_with_llm(user_request: str, available_agents: List[str]) -> Optional[List[Dict]]:
    if not available_agents or not OLLAMA_AVAILABLE:
        return None

    agent_list = ', '.join(available_agents)

    prompt = f'''You are a task planner for UniNexus AI, a university intelligence platform.

AVAILABLE AGENTS:
- AttendanceAgent: fetches students with LOW attendance (below a threshold). Use when the user asks about attendance.
- PolicyAgent: retrieves university policy rules (attendance policy, exam rules, etc.). Use when the user asks about rules or policies.
- RiskAgent: identifies at-risk students using attendance AND grades. Use when the user asks about risk, failure, or academic difficulty.
- KnowledgeAgent: searches written university documents for answers. Use when the user needs text content or a policy explanation.

RULES:
1. Choose ONLY from: {agent_list}
2. Match agents to the user's actual intent. DO NOT always pick the same agents.
3. If the user asks about attendance → use AttendanceAgent.
4. If the user asks about a POLICY or RULE → use KnowledgeAgent and/or PolicyAgent.
5. If the user asks about which students might fail or are at risk → use RiskAgent.
6. If the user asks "show students" → use AttendanceAgent first.
7. If the user says "NOT" or "excluding", still use the relevant agent — we filter results later.
8. Maximum 4 steps.

EXAMPLES:

User: "Show students with low attendance"
Plan: [{{"step": 1, "agent": "AttendanceAgent", "action": "Fetch students with low attendance"}}]

User: "What is the exam policy?"
Plan: [{{"step": 1, "agent": "KnowledgeAgent", "action": "Search exam policy documents"}}]

User: "Which students might fail?"
Plan: [{{"step": 1, "agent": "RiskAgent", "action": "Identify at-risk students"}}]

User: "Tell me about the attendance policy"
Plan: [{{"step": 1, "agent": "KnowledgeAgent", "action": "Search attendance policy document"}}]

NOW YOUR TURN:

User: "{user_request}"

Return JSON with a "plan" field. Each step needs: "step", "agent", "action". Respond with JSON only.'''

    try:
        response = ollama.generate(
            model=DEFAULT_MODEL,
            prompt=prompt,
            format='json',
            options={'temperature': 0.1},
            keep_alive='30m'
        )
        raw = response.get('response', '') if isinstance(response, dict) else getattr(response, 'response', '')
        if not raw:
            return None
        data = json.loads(raw)
        plan = data.get('plan') if isinstance(data, dict) else data
        if not isinstance(plan, list) or not plan:
            return None
        valid_agents = set(available_agents)
        for step in plan:
            if not isinstance(step, dict):
                return None
            if step.get('agent') not in valid_agents:
                logger.warning(f'LLM chose invalid agent: {step.get("agent")}')
                return None
            if 'step' not in step or 'action' not in step:
                return None
        return plan
    except Exception as e:
        logger.error(f'LLM planning failed: {e}')
        return None

def generate_completion(prompt: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    if not OLLAMA_AVAILABLE:
        return None
    try:
        response = ollama.generate(model=model, prompt=prompt, options={'temperature': 0.1})
        if isinstance(response, dict):
            return response.get('response', '')
        return getattr(response, 'response', None)
    except Exception as e:
        logger.error(f'Ollama generation failed: {e}')
        return None
