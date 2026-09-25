"""
English: Thin wrapper around the LLM gateway with dual-mode planning.
Roman Urdu: LLM gateway ke upar ek thin wrapper jisme dual-mode planning hai.
"""
import json
import logging
from typing import Optional, List, Dict, Any

from backend.app.core.llm_gateway import get_gateway

logger = logging.getLogger(__name__)

# English: System context so the LLM knows what UniNexus AI is.
# Roman Urdu: System context taake LLM ko pata ho UniNexus AI kya hai.
SYSTEM_CONTEXT = """UniNexus AI is an autonomous multi-agent university intelligence platform built by Zarak Khan (2026).

Its purpose:
- Help universities monitor student attendance, academic risk, and institutional policies
- Orchestrate specialized AI agents that query real university data
- Provide intelligent answers using a multi-provider LLM gateway (Groq, Gemini, Ollama)
- Built with FastAPI (backend), React (frontend), SQLAlchemy (database)

Its 4 specialized agents:
- AttendanceAgent: finds students with low attendance
- PolicyAgent: returns institutional policy rules and thresholds
- RiskAgent: analyzes academic risk from attendance + grades
- KnowledgeAgent: searches university documents (handbook, policies, exam rules)

Users interact via the AI Command Center by typing natural-language requests."""


def check_ollama_status() -> Dict[str, Any]:
    """Kept for backward compatibility — returns the gateway's full status."""
    try:
        gw = get_gateway()
        status = gw.status()
        return {
            "available": status.get("primary_available", False) or status.get("ollama_status", {}).get("available", False),
            "default_model": status.get("primary_model") or status.get("ollama_status", {}).get("model", "unknown"),
            "model_ready": status.get("primary_available", False),
            "installed_models": status.get("ollama_status", {}).get("installed_models", []),
            "gateway": status,
        }
    except Exception as e:
        logger.error(f"LLM status check failed: {e}")
        return {"available": False, "default_model": "unknown", "model_ready": False, "installed_models": [], "reason": str(e)}


def generate_completion(prompt: str, model: str = None) -> Optional[str]:
    """Raw completion via the gateway."""
    try:
        gw = get_gateway()
        resp = gw.generate(prompt, json_mode=False)
        return resp.text if resp.success else None
    except Exception as e:
        logger.error(f"generate_completion exception: {e}")
        return None


def plan_with_llm(user_request: str, available_agents: List[str]) -> Optional[Dict]:
    """
    English: Ask the LLM to decide between agent workflow and direct answer.
             Returns a dict with 'mode', 'plan', and 'answer' keys, or None on failure.
    Roman Urdu: LLM se poocho ke agent workflow chalana hai ya direct jawab dena hai.
             Dict return karta hai jisme 'mode', 'plan', 'answer' keys hain, ya None.
    """
    if not available_agents:
        return None

    agent_list = ", ".join(available_agents)

    prompt = f"""{SYSTEM_CONTEXT}

You are the orchestrator. Decide how to handle the user's request.

Available agents: {agent_list}

DECISION RULES:
1. If the request is about ATTENDANCE, POLICY, RISK, or UNIVERSITY DOCUMENTS
   → mode = "agent_workflow", choose ONLY the relevant agents (1 to 4, not all)

2. If the request is:
   - A casual greeting or chit-chat
   - A meta-question about the system itself (what is this? how does it work? who built it?)
   - General knowledge unrelated to university data
   - Or anything the agents cannot meaningfully answer
   → mode = "direct_answer", answer briefly in 1-3 sentences

3. NEVER use all 4 agents "just in case". Only what's needed.

Return STRICT JSON with this exact shape:
{{
  "mode": "agent_workflow" or "direct_answer",
  "plan": [{{"step": 1, "agent": "AgentName", "action": "short action"}}],
  "answer": "short plain-text answer, or empty string"
}}

For agent_workflow: plan has 1-4 steps, answer is "".
For direct_answer: plan is [], answer has the 1-3 sentence response.

User request: "{user_request}"

Respond with JSON only."""

    try:
        gw = get_gateway()
        resp = gw.generate(prompt, json_mode=True)

        if not resp.success or not resp.text:
            logger.warning(f"LLM planning failed via {resp.provider}: {resp.error}")
            return None

        raw = resp.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.lower().startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        data = json.loads(raw)

        # English: Normalise the shape — accept plan-only fallback for old models.
        # Roman Urdu: Shape ko normalize karo — purane models ke liye sirf plan bhi accept karo.
        mode = data.get("mode", "agent_workflow")
        plan = data.get("plan") or []
        answer = (data.get("answer") or "").strip()

        if mode == "direct_answer":
            if not answer:
                return None
            logger.info(f"LLM direct answer via {resp.provider} ({resp.model})")
            return {"mode": "direct_answer", "plan": [], "answer": answer}

        # agent_workflow mode
        if not isinstance(plan, list) or not plan:
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
        return {"mode": "agent_workflow", "plan": plan, "answer": ""}

    except json.JSONDecodeError as e:
        logger.error(f"LLM returned invalid JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"LLM planning exception: {e}")
        return None
