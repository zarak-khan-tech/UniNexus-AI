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

def plan_with_llm(user_request: str, available_agents: List[str]) -> Optional[List[Dict]]:
    if not available_agents or not OLLAMA_AVAILABLE:
        return None

    agent_list = ', '.join(available_agents)

    prompt = f'''You plan tasks for a university AI system.

Agents available: {agent_list}

Rules:
- AttendanceAgent: students with low attendance
- PolicyAgent: institutional policy rules
- RiskAgent: academic risk analysis
- KnowledgeAgent: search university documents

User question: "{user_request}"

Return a JSON object with a "plan" field containing an array of steps.
Each step: {{"step": 1, "agent": "AgentName", "action": "short text"}}.

Respond with JSON only.'''

    try:
        response = ollama.generate(
            model=DEFAULT_MODEL,
            prompt=prompt,
            format='json',
            options={'temperature': 0.1}
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
