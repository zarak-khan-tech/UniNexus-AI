"""
English: Reasoning loop — reads active tools from tenant DB, respects tool 
disabled state, tracks RAG sources, multi-turn memory, tenant thresholds.
Roman Urdu: Reasoning loop — tenant DB se active tools padhta hai, tool 
disable state respect karta hai, RAG sources track karta hai.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from backend.app.core.llm_gateway import get_gateway
from backend.app.services.tenant_settings import get_tenant_settings
from backend.app.services.tool_definitions import list_tool_definitions
from backend.app.tools import tool_registry

logger = logging.getLogger(__name__)
MAX_ITERATIONS = 5
MAX_HISTORY_TURNS = 6

BASE_PROMPT = """You are the reasoning core of UniNexus AI, a multi-agent 
university intelligence platform.

You have access to TOOLS. To answer:
1. Think about what information you need.
2. Call tools with the right arguments.
3. Look at results. Call more tools if needed.
4. Produce a final answer USING ONLY FACTS FROM THE TOOL RESULTS.

UNIVERSITY CONTEXT (from this tenant's settings — use these values):
- Attendance threshold: {attendance_threshold}% — students below this are considered low-attendance.
- Risk HIGH threshold: below {risk_high_threshold}% attendance OR failing grade (D/F) → High risk.
- Risk MEDIUM threshold: below {risk_medium_threshold}% attendance OR C grade → Medium risk.
- University name: {university_name}

When the user asks about attendance or risk WITHOUT specifying a number, 
use the university's configured thresholds above (not your own guesses).

CRITICAL RULE — ALWAYS CALL A TOOL WHEN THE USER ASKS ABOUT DATA:
If the user asks for ACTUAL DATA (students, attendance, grades, courses, policies), 
you MUST call a tool. Never say "I don't have that information" without trying a tool.

Phrases that REQUIRE a tool call:
- "show me students..." -> attendance_query or list_students
- "which students..." / "who is..." -> attendance_query or list_enrollments
- "which might fail" / "at risk" -> list_enrollments
- "what does the policy say" / "rules about" -> semantic_search
- "what is the definition of X" / "passing grade" / "minimum CGPA" -> semantic_search FIRST

ANTI-HALLUCINATION:
- If a fact is NOT in the tool results, DO NOT invent it.
- When stating a policy, QUOTE or closely paraphrase the actual text.
- Always cite the source by title.

EVIDENCE QUALITY (from semantic_search results):
Every semantic_search result includes an "evidence_quality" field:
- "strong"  → answer confidently, quote directly, cite the document.
- "weak"    → answer cautiously: "Based on related material, it appears that... 
              but I could not find a document that directly addresses this. 
              Please verify with the registrar."
- "none"    → do NOT answer from general knowledge. Say: "I could not find 
              relevant information in the university's knowledge base. 
              Please check with the appropriate office."
NEVER invent policies or rules when evidence is weak or missing.

HIGH-RISK ACTIONS REQUIRE APPROVAL:
- Tools marked write_high (e.g. update_student_grade) do NOT execute immediately.
- They are queued for human approval. Tell the user it's been queued. Do NOT call again.

Available tools:
{tools_desc}

Respond with STRICT JSON in one of these two shapes:
A) To call a tool:
{{"action": "tool_call", "tool": "tool_name", "args": {{...}}, "reasoning": "why"}}
B) When ready to answer:
{{"action": "final_answer", "answer": "your grounded answer, citing sources"}}
"""


def _strip_json_fences(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            raw = parts[1]
            if raw.lower().startswith("json"):
                raw = raw[4:]
    return raw.strip()


def _format_tools_for_llm(tenant_id: Optional[int]) -> str:
    """
    English: Read active tool definitions for this tenant from DB; fall back 
    to class registry if DB has no rows. Filters out disabled tools.
    Roman Urdu: Tenant ke active tool definitions DB se padho; agar rows na 
    hon to class registry fallback. Disabled tools filter karo.
    """
    tools_meta = None
    if tenant_id:
        try:
            tools_meta = list_tool_definitions(tenant_id, active_only=True)
        except Exception as e:
            logger.warning(f"Failed to read tenant tool defs: {e}")
    if not tools_meta:
        tools_meta = tool_registry.list()

    lines = []
    for t in tools_meta:
        schema = t.get('input_schema') or {}
        props = schema.get('properties', {}) if isinstance(schema, dict) else {}
        arg_str = ', '.join([f"{k}: {v.get('type', 'any')}" for k, v in props.items()]) or 'no args'
        lines.append(f"- {t['name']} ({t['permission']}): {t['description']} | args: {arg_str}")
    return '\n'.join(lines)


def _format_history(history: Optional[List[Dict[str, Any]]]) -> str:
    if not history:
        return ""
    recent = history[-MAX_HISTORY_TURNS:]
    lines = ["CONVERSATION HISTORY (most recent last):"]
    for turn in recent:
        role = (turn.get('role') or 'user').capitalize()
        content = (turn.get('content') or '')[:600]
        lines.append(f"- {role}: {content}")
    lines.append("")
    lines.append("Use this history to resolve pronouns (them/those/it) and to maintain continuity.")
    lines.append("")
    return '\n'.join(lines)


def _build_system_prompt(settings: Dict[str, Any], tenant_id: Optional[int]) -> str:
    tools_desc = _format_tools_for_llm(tenant_id)
    return BASE_PROMPT.format(
        attendance_threshold=settings.get('attendance_threshold', 75),
        risk_high_threshold=settings.get('risk_high_threshold', 60),
        risk_medium_threshold=settings.get('risk_medium_threshold', 75),
        university_name=settings.get('university_name', 'the university'),
        tools_desc=tools_desc,
    )


def _extract_sources_from_tool_result(tool_name: str, result_data: Any) -> List[Dict[str, Any]]:
    if tool_name != 'semantic_search' or not isinstance(result_data, list):
        return []
    sources = []
    for doc in result_data:
        if not isinstance(doc, dict):
            continue
        title = doc.get('title')
        if not title:
            continue
        sources.append({
            'title': title,
            'category': doc.get('category'),
            'similarity': doc.get('similarity'),
        })
    return sources


def _dedupe_sources(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_title: Dict[str, Dict[str, Any]] = {}
    for s in sources:
        t = s.get('title')
        if not t:
            continue
        if t not in by_title or (s.get('similarity') or 0) > (by_title[t].get('similarity') or 0):
            by_title[t] = s
    return sorted(by_title.values(), key=lambda x: x.get('similarity') or 0, reverse=True)


def _create_approval(user_id: int, user_email: str, tenant_id: int,
                     tool_name: str, args: Dict[str, Any],
                     action_description: str, reasoning: str) -> int:
    from backend.app.core.database import SessionLocal
    from backend.app.models.approval import Approval
    db = SessionLocal()
    try:
        approval = Approval(
            tenant_id=tenant_id, user_id=user_id, user_email=user_email,
            tool_name=tool_name, args_json=json.dumps(args),
            action_description=action_description, reasoning=reasoning,
            status='pending',
        )
        db.add(approval)
        db.commit()
        db.refresh(approval)
        try:
            from backend.app.services.notifications import create_notification
            create_notification(
                tenant_id=tenant_id, user_id=user_id, kind='approval',
                title='New approval request',
                body=f'{tool_name.replace("_", " ").title()} requires your review.',
                action_url='/approvals',
            )
        except Exception:
            pass
        return approval.id
    finally:
        db.close()


def _is_tool_active(tenant_id: Optional[int], tool_name: str) -> bool:
    """
    English: True if this tool is enabled for the tenant. If DB has no 
    definition row, allow (class registry fallback).
    Roman Urdu: True agar tool tenant ke liye enabled hai. Agar DB mein row 
    na ho to allow karo (class registry fallback).
    """
    if not tenant_id:
        return True
    try:
        rows = list_tool_definitions(tenant_id, active_only=False)
        for r in rows:
            if r['name'] == tool_name:
                return bool(r.get('is_active', True))
        # Not present in DB — fall back to registry existence
        return tool_registry.get(tool_name) is not None
    except Exception:
        return True



# English: Detect answers that cite sources even though no tool returned any.
# Roman Urdu: Aisi answers detect karo jo sources cite karein lekin koi tool 
# ne kuch return na kiya ho.
_HALLUCINATION_PHRASES = (
    'according to the',
    'per the university',
    'source:',
    'the university policy states',
    'the policy says',
    'as stated in the',
    'strong evidence',
)


def _looks_like_hallucination(answer: str, collected_sources: list) -> bool:
    """
    English: True if the answer cites sources/policies but we collected none.
    Roman Urdu: True agar answer sources/policies cite kare lekin humne koi 
    collect nahi kiya.
    """
    if collected_sources:
        return False
    lowered = (answer or '').lower()
    return any(p in lowered for p in _HALLUCINATION_PHRASES)


def reason(user_request: str, history: Optional[List[Dict[str, Any]]] = None,
           user_id: Optional[int] = None, user_email: Optional[str] = None,
           tenant_id: Optional[int] = None) -> Dict[str, Any]:
    settings = get_tenant_settings(tenant_id) if tenant_id else {}
    system = _build_system_prompt(settings, tenant_id)
    gw = get_gateway()
    history_block = _format_history(history)
    conversation = (
        f"{history_block}"
        f"User question: {user_request}\n\n"
        f"Your turn. Respond with JSON only."
    )
    tool_calls_log: List[Dict[str, Any]] = []
    collected_sources: List[Dict[str, Any]] = []
    pending_approval_id: Optional[int] = None

    for iteration in range(1, MAX_ITERATIONS + 1):
        resp = gw.generate(system + "\n\n" + conversation, json_mode=True)
        if not resp.success or not resp.text:
            logger.warning(f"Reasoning failed at iteration {iteration}: {resp.error}")
            return {
                "answer": "I could not complete the reasoning. Please try again.",
                "tool_calls": tool_calls_log, "iterations": iteration,
                "error": resp.error, "sources": _dedupe_sources(collected_sources),
            }

        raw = _strip_json_fences(resp.text)
        try:
            decision = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"Bad JSON: {e}. Raw: {raw[:200]}")
            return {
                "answer": "I had trouble parsing my own reasoning. Please retry.",
                "tool_calls": tool_calls_log, "iterations": iteration,
                "error": "invalid_json", "sources": _dedupe_sources(collected_sources),
            }

        action = decision.get("action")

        if action == "final_answer":
            answer = (decision.get("answer") or "").strip()

            # English: Hallucination guard — reject answers that cite 
            # sources when no sources were collected.
            # Roman Urdu: Hallucination guard — agar koi source collect 
            # na hua ho aur answer sources cite kare, to reject karo.
            if _looks_like_hallucination(answer, collected_sources):
                logger.warning(
                    "Hallucination guard triggered at iteration "
                    f"{iteration} — rejecting source-citing answer with no "
                    "collected sources."
                )
                conversation += (
                    "\n\n[Correction] Your previous answer cited sources "
                    "or policies, but you did NOT call semantic_search "
                    "(or it returned no results). This is a hallucination. "
                    "You MUST either: (a) call semantic_search to retrieve "
                    "real documents, or (b) reply honestly that the "
                    "information is not in the knowledge base. Do NOT "
                    "invent policies or credentials."
                )
                continue

            return {
                "answer": answer or "No answer generated.",
                "tool_calls": tool_calls_log, "iterations": iteration,
                "provider": resp.provider, "model": resp.model,
                "pending_approval_id": pending_approval_id,
                "sources": _dedupe_sources(collected_sources),
            }

        if action == "tool_call":
            tool_name = decision.get("tool")
            args = decision.get("args") or {}
            reasoning = decision.get("reasoning", "")
            tool = tool_registry.get(tool_name)

            if not tool:
                tool_calls_log.append({
                    "iteration": iteration, "tool": tool_name, "args": args,
                    "reasoning": reasoning,
                    "summary": {"success": False, "error": "unknown tool"},
                })
                conversation += f"\n\n[Iteration {iteration}] Error: tool '{tool_name}' does not exist."
                continue

            # English: Block disabled tools at execution time (belt + suspenders).
            # Roman Urdu: Disabled tools ko execution time pe block karo.
            if not _is_tool_active(tenant_id, tool_name):
                tool_calls_log.append({
                    "iteration": iteration, "tool": tool_name, "args": args,
                    "reasoning": reasoning,
                    "summary": {"success": False, "error": "tool_disabled"},
                })
                conversation += (
                    f"\n\n[Iteration {iteration}] Error: tool '{tool_name}' is disabled for this tenant."
                    f" Do not call it. Choose another tool or produce final_answer."
                )
                continue

            from backend.app.tools.base import PermissionLevel
            if tool.permission == PermissionLevel.WRITE_HIGH:
                desc = f"Call {tool_name} with args: {json.dumps(args)}"
                approval_id = _create_approval(
                    user_id=user_id or 0, user_email=user_email or 'unknown',
                    tenant_id=tenant_id or 1, tool_name=tool_name,
                    args=args, action_description=desc, reasoning=reasoning,
                )
                pending_approval_id = approval_id
                tool_calls_log.append({
                    "iteration": iteration, "tool": tool_name, "args": args,
                    "reasoning": reasoning,
                    "summary": {"success": True, "queued_for_approval": True, "approval_id": approval_id},
                })
                fake = {
                    "status": "pending_approval", "approval_id": approval_id,
                    "message": "Queued for human approval. Tell the user. Do NOT call again.",
                }
                conversation += (
                    f"\n\n[Iteration {iteration}] You called tool '{tool_name}' with args {json.dumps(args)}.\n"
                    f"Result:\n{json.dumps(fake)}\n\nNow produce final_answer telling the user it's queued."
                )
                continue

            result = tool_registry.call(tool_name, **args)
            summary = {
                "success": result.success,
                "count": result.metadata.get("count") if result.metadata else None,
                "error": result.error,
            }
            tool_calls_log.append({
                "iteration": iteration, "tool": tool_name, "args": args,
                "reasoning": reasoning, "summary": summary,
            })

            if tool_name == 'semantic_search' and result.success and result.data:
                extracted = _extract_sources_from_tool_result(tool_name, result.data)
                collected_sources.extend(extracted)

            result_text = json.dumps({
                "success": result.success, "data": result.data,
                "metadata": result.metadata, "error": result.error,
            }, default=str)
            if len(result_text) > 30000:
                result_text = result_text[:30000] + '...[truncated]'

            conversation += (
                f"\n\n[Iteration {iteration}] You called tool '{tool_name}' with args {json.dumps(args)}.\n"
                f"Result:\n{result_text}\n\nNow decide: call another tool or produce final_answer."
            )
            continue

        return {
            "answer": "I produced an unexpected reasoning step. Please retry.",
            "tool_calls": tool_calls_log, "iterations": iteration,
            "error": f"unknown_action:{action}",
            "sources": _dedupe_sources(collected_sources),
        }

    return {
        "answer": "I reached the maximum reasoning steps.",
        "tool_calls": tool_calls_log, "iterations": MAX_ITERATIONS,
        "error": "max_iterations", "pending_approval_id": pending_approval_id,
        "sources": _dedupe_sources(collected_sources),
    }
