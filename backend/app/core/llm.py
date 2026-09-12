import json
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

DEFAULT_MODEL = 'llama3.2:1b'

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
        model_ready = any(DEFAULT_MODEL in (n or '') for n in model_names)
        return {
            'available': True,
            'default_model': DEFAULT_MODEL,
            'model_ready': model_ready,
            'installed_models': model_names,
        }
    except Exception as e:
        return {'available': False, 'reason': str(e)}

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

def plan_with_llm(user_request: str, available_agents: List[str]) -> Optional[List[Dict]]:
    if not available_agents:
        return None
    agent_list = '\n'.join(f'- {a}' for a in available_agents)
    prompt = f'''You are the orchestrator of a multi-agent university AI platform.

Available agents:
{agent_list}

Agent responsibilities:
- AttendanceAgent: retrieves students with low attendance
- PolicyAgent: looks up institutional policy rules and thresholds
- RiskAgent: analyzes academic risk using attendance and grades
- KnowledgeAgent: searches university policy documents

User request: "{user_request}"

Task: Return ONLY a valid JSON array of steps.

Rules:
1. Use ONLY agents from the list above.
2. Each step needs: "step" (int), "agent" (exact name), "action" (short text).
3. Keep to 1-4 steps.
4. Return ONLY raw JSON. No markdown, no code fences.

Example: [{{"step": 1, "agent": "KnowledgeAgent", "action": "Search policies"}}]

Your JSON:'''
    raw = generate_completion(prompt)
    if not raw:
        return None
    try:
        start = raw.find('[')
        end = raw.rfind(']') + 1
        if start == -1 or end <= start:
            return None
        plan = json.loads(raw[start:end])
        if not isinstance(plan, list) or not plan:
            return None
        valid_agents = set(available_agents)
        for step in plan:
            if not isinstance(step, dict):
                return None
            if step.get('agent') not in valid_agents:
                return None
            if 'step' not in step or 'action' not in step:
                return None
        return plan
    except Exception as e:
        logger.error(f'Failed to parse LLM plan: {e}')
        return None
