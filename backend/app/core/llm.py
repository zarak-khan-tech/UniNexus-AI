"""
English: Thin wrapper around the LLM gateway with dual-mode planning.
Roman Urdu: LLM gateway ke upar thin wrapper, dual-mode planning ke saath.
"""
import json
import logging
from typing import Optional, List, Dict, Any
from backend.app.core.llm_gateway import get_gateway

logger = logging.getLogger(__name__)

SYSTEM_CONTEXT = """UniNexus AI is an autonomous multi-agent university intelligence platform built by Zarak Khan (2026).
Its purpose:
- Help universities monitor attendance, academic risk, and institutional policies
- Orchestrate specialized agents that query real university data
- Provide intelligent answers using a multi-provider LLM gateway (Groq, Gemini, Ollama)
Built with FastAPI (backend), React (frontend), SQLAlchemy (database)."""

def check_ollama_status() -> Dict[str, Any]:
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
    Roman Urdu: LLM se poocho ke agent workflow chalana hai ya direct jawab dena hai.
    """
    if not available_agents:
        return None

    agent_list = ", ".join(available_agents)

    prompt = f"""{SYSTEM_CONTEXT}

You are the orchestrator. Decide how to handle the user's request.

AVAILABLE AGENTS:
- AttendanceAgent: queries the DB for students whose attendance is below a threshold. Use ONLY when the user asks about WHICH STUDENTS have low attendance.
- PolicyAgent: returns a single NUMERIC threshold rule (e.g., "minimum 75% attendance required"). Use ONLY for very short numeric threshold questions like "what is the minimum attendance".
- RiskAgent: queries the DB for students at risk based on attendance + grades. Use ONLY when the user asks about WHICH STUDENTS are at risk or might fail.
- KnowledgeAgent: performs SEMANTIC search over university documents (handbooks, exam rules, fee policy, hostel rules, leave of absence, grading, etc.). Returns real document text with similarity scores. Use this for ANY question that asks "what are the rules", "what happens if", "tell me about", "how do I", "can I" — anything that needs an actual policy/document answer.

CRITICAL ROUTING RULES:
1. "what happens if I fail an exam" → KnowledgeAgent (search exam rules)
2. "how much does semester cost" → KnowledgeAgent (search fee policy)
3. "can I take a break from studies" → KnowledgeAgent (search leave of absence)
4. "what is the minimum attendance percentage" → PolicyAgent (numeric threshold only)
5. "show me students with low attendance" → AttendanceAgent
6. "which students might fail" → RiskAgent
7. "hello" or "what is this system" → mode=direct_answer

DECISION MODES:
- If the request needs one or more agents → mode="agent_workflow"
- If it's casual chit-chat or a meta-question about the system → mode="direct_answer"

Return STRICT JSON:
{{
  "mode": "agent_workflow" or "direct_answer",
  "plan": [{{"step": 1, "agent": "AgentName", "action": "short action"}}],
  "answer": "short plain-text answer, or empty string"
}}

For agent_workflow: plan has 1-3 steps. Answer is "".
For direct_answer: plan is []. Answer has 1-3 sentences.

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
        mode = data.get("mode", "agent_workflow")
        plan = data.get("plan") or []
        answer = (data.get("answer") or "").strip()

        if mode == "direct_answer":
            if not answer:
                return None
            logger.info(f"LLM direct answer via {resp.provider} ({resp.model})")
            return {"mode": "direct_answer", "plan": [], "answer": answer}

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
