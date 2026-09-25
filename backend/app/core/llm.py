"""
English: Thin wrapper around the LLM gateway. Keeps the same public functions so
        existing code (orchestrator, endpoints) needs zero changes.
Roman Urdu: LLM gateway ke upar ek thin wrapper. Same public functions rakhta hai
        taake existing code (orchestrator, endpoints) mein koi change na karna pare.
"""
import json
import logging
from typing import Optional, List, Dict, Any

from backend.app.core.llm_gateway import get_gateway

logger = logging.getLogger(__name__)


def check_ollama_status() -> Dict[str, Any]:
    """
    English: Kept for backward compatibility. Returns the gateway's full status.
    Roman Urdu: Purane naam ke liye rakha hai. Gateway ka poora status return karta hai.
    """
    try:
        gw = get_gateway()
        status = gw.status()

        # English: Map to the older shape used by the frontend badge.
        # Roman Urdu: Frontend badge jo purana shape use karta hai usi mein map karo.
        return {
            "available": status.get("primary_available", False) or status.get("ollama_status", {}).get("available", False),
            "default_model": status.get("primary_model") or status.get("ollama_status", {}).get("model", "unknown"),
            "model_ready": status.get("primary_available", False),
            "installed_models": status.get("ollama_status", {}).get("installed_models", []),
            # English: Also include the richer gateway info.
            # Roman Urdu: Naya richer gateway info bhi include karo.
            "gateway": status,
        }
    except Exception as e:
        logger.error(f"LLM status check failed: {e}")
        return {
            "available": False,
            "default_model": "unknown",
            "model_ready": False,
            "installed_models": [],
            "reason": str(e),
        }


def generate_completion(prompt: str, model: str = None) -> Optional[str]:
    """
    English: Raw completion via the gateway. Kept for any code that still uses it.
    Roman Urdu: Gateway se raw completion. Purane code ke liye rakha hai.
    """
    try:
        gw = get_gateway()
        resp = gw.generate(prompt, json_mode=False)
        if resp.success:
            return resp.text
        logger.warning(f"generate_completion failed: {resp.error}")
        return None
    except Exception as e:
        logger.error(f"generate_completion exception: {e}")
        return None


def plan_with_llm(user_request: str, available_agents: List[str]) -> Optional[List[Dict]]:
    """
    English: Ask the LLM (Gemini first, Ollama fallback) to produce a structured plan.
             Returns a validated plan list, or None if parsing/validation fails.
    Roman Urdu: LLM se (pehle Gemini, phir Ollama) structured plan maango.
             Validated plan list return karo, ya None agar parsing/validation fail ho.
    """
    if not available_agents:
        return None

    agent_list = ", ".join(available_agents)

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
        gw = get_gateway()
        resp = gw.generate(prompt, json_mode=True)

        if not resp.success or not resp.text:
            logger.warning(f"LLM planning failed via {resp.provider}: {resp.error}")
            return None

        raw = resp.text.strip()

        # English: Some models wrap JSON in markdown code fences — strip them.
        # Roman Urdu: Kuch models JSON ko markdown fence mein daalte hain — unko nikaalo.
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.lower().startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        data = json.loads(raw)
        plan = data.get("plan") if isinstance(data, dict) else data

        if not isinstance(plan, list) or not plan:
            logger.warning(f"LLM returned invalid plan shape: {str(plan)[:200]}")
            return None

        valid_agents = set(available_agents)
        for step in plan:
            if not isinstance(step, dict):
                return None
            if step.get("agent") not in valid_agents:
                logger.warning(f"LLM chose unknown agent: {step.get('agent')}")
                return None
            if "step" not in step or "action" not in step:
                return None

        logger.info(f"LLM planned via {resp.provider} ({resp.model}): {len(plan)} steps")
        return plan

    except json.JSONDecodeError as e:
        logger.error(f"LLM returned invalid JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"LLM planning exception: {e}")
        return None
