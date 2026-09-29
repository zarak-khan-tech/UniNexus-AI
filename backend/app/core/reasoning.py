"""
English: Real agentic reasoning loop with memory and human-approval gating
         for high-risk actions.
Roman Urdu: Real agentic reasoning loop — memory aur high-risk actions ke liye
            human approval gating ke saath.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from backend.app.tools import tool_registry
from backend.app.tools.base import PermissionLevel
from backend.app.core.llm_gateway import get_gateway

logger = logging.getLogger(__name__)
MAX_ITERATIONS = 5
MAX_HISTORY_TURNS = 6


SYSTEM_PROMPT = """You are the reasoning core of UniNexus AI, a multi-agent 
university intelligence platform.

You have access to TOOLS. To answer:
1. Think about what information you need.
2. Call tools with the right arguments.
3. Look at results. Call more tools if needed.
4. Produce a final answer USING ONLY FACTS FROM THE TOOL RESULTS.

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
- Always cite the source: "Per the Grading System Guidelines..." 

HIGH-RISK ACTIONS REQUIRE APPROVAL:
- Some tools are marked HIGH-RISK (write_high) — e.g. update_student_grade.
- When you call a high-risk tool, it will NOT execute immediately. Instead, it will 
  return a message saying the action is queued for human approval.
- In that case, tell the user: "I've queued this action for admin approval. 
  It will execute once approved." Do NOT try to call the tool again.

Available tools:
{tools_desc}

Respond with STRICT JSON in one of these two shapes:

A) To call a tool:
{{"action": "tool_call", "tool": "tool_name", "args": {{...}}, "reasoning": "why"}}

B) When ready to answer:
{{"action": "final_answer", "answer": "your grounded answer, citing sources"}}
"""


def _format_tools_for_llm() -> str:
    lines = []
    for t in tool_registry.list():
        args = t.get('input_schema', {}).get('properties', {})
        arg_str = ', '.join([f"{k}: {v.get('type', 'any')}" for k, v in args.items()]) or 'no args'
        lines.append(f"- {t['name']} ({t['permission']}): {t['description']} | args: {arg_str}")
    return '\n'.join(lines)


def _strip_json_fences(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            raw = parts[1]
        if raw.lower().startswith("json"):
            raw = raw[4:]
    return raw.strip()


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


def _create_approval(user_id: int, user_email: str, tenant_id: int,
                     tool_name: str, args: Dict[str, Any],
                     action_description: str, reasoning: str) -> int:
    """
    English: Persist a pending approval for a WRITE_HIGH action.
    Roman Urdu: WRITE_HIGH action ke liye pending approval save karo.
    """
    from backend.app.core.database import SessionLocal
    from backend.app.models.approval import Approval
    db = SessionLocal()
    try:
        approval = Approval(
            tenant_id=tenant_id,
            user_id=user_id,
            user_email=user_email,
            tool_name=tool_name,
            args_json=json.dumps(args),
            action_description=action_description,
            reasoning=reasoning,
            status='pending',
        )
        db.add(approval)
        db.commit()
        db.refresh(approval)

        try:
            from backend.app.services.notifications import create_notification
            create_notification(
                tenant_id=tenant_id,
                user_id=user_id,
                kind='approval',
                title='New approval request',
                body=f'{tool_name.replace("_", " ").title()} requires your review.',
                action_url='/approvals',
            )
        except Exception:
            pass

        return approval.id
    finally:
        db.close()


def reason(user_request: str, history: Optional[List[Dict[str, Any]]] = None,
           user_id: Optional[int] = None, user_email: Optional[str] = None,
           tenant_id: Optional[int] = None) -> Dict[str, Any]:
    gw = get_gateway()
    tools_desc = _format_tools_for_llm()
    system = SYSTEM_PROMPT.replace("{tools_desc}", tools_desc)
    history_block = _format_history(history)
    conversation = (
        f"{history_block}"
        f"User question: {user_request}\n\n"
        f"Your turn. Respond with JSON only."
    )
    tool_calls_log: List[Dict[str, Any]] = []
    pending_approval_id: Optional[int] = None

    for iteration in range(1, MAX_ITERATIONS + 1):
        resp = gw.generate(system + "\n\n" + conversation, json_mode=True)
        if not resp.success or not resp.text:
            logger.warning(f"Reasoning failed at iteration {iteration}: {resp.error}")
            return {
                "answer": "I could not complete the reasoning. Please try again.",
                "tool_calls": tool_calls_log,
                "iterations": iteration,
                "error": resp.error,
            }

        raw = _strip_json_fences(resp.text)
        try:
            decision = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"Bad JSON: {e}. Raw: {raw[:200]}")
            return {
                "answer": "I had trouble parsing my own reasoning. Please retry.",
                "tool_calls": tool_calls_log,
                "iterations": iteration,
                "error": "invalid_json",
            }

        action = decision.get("action")

        if action == "final_answer":
            answer = (decision.get("answer") or "").strip()
            return {
                "answer": answer or "No answer generated.",
                "tool_calls": tool_calls_log,
                "iterations": iteration,
                "provider": resp.provider,
                "model": resp.model,
                "pending_approval_id": pending_approval_id,
            }

        if action == "tool_call":
            tool_name = decision.get("tool")
            args = decision.get("args") or {}
            reasoning = decision.get("reasoning", "")

            tool = tool_registry.get(tool_name)
            if not tool:
                # Unknown tool — log and continue
                tool_calls_log.append({
                    "iteration": iteration, "tool": tool_name, "args": args,
                    "reasoning": reasoning,
                    "summary": {"success": False, "error": "unknown tool"},
                })
                conversation += f"\n\n[Iteration {iteration}] Error: tool '{tool_name}' does not exist."
                continue

            # English: HIGH-RISK actions are intercepted — approval required.
            # Roman Urdu: HIGH-RISK actions intercept hote hain — approval zaroori.
            if tool.permission == PermissionLevel.WRITE_HIGH:
                desc = f"Call {tool_name} with args: {json.dumps(args)}"
                approval_id = _create_approval(
                    user_id=user_id or 0,
                    user_email=user_email or 'unknown',
                    tenant_id=tenant_id or 1,
                    tool_name=tool_name,
                    args=args,
                    action_description=desc,
                    reasoning=reasoning,
                )
                pending_approval_id = approval_id

                tool_calls_log.append({
                    "iteration": iteration, "tool": tool_name, "args": args,
                    "reasoning": reasoning,
                    "summary": {
                        "success": True,
                        "count": None,
                        "queued_for_approval": True,
                        "approval_id": approval_id,
                    },
                })

                fake_result = {
                    "status": "pending_approval",
                    "approval_id": approval_id,
                    "message": (
                        "This action was queued for human approval. "
                        "It will execute once an administrator approves. "
                        "Tell the user it's been queued — do NOT call this tool again."
                    ),
                }
                conversation += (
                    f"\n\n[Iteration {iteration}] You called tool '{tool_name}' "
                    f"with args {json.dumps(args)}.\nResult:\n{json.dumps(fake_result)}\n\n"
                    f"Now produce final_answer informing the user this was queued for approval."
                )
                continue

            # English: READ / WRITE_LOW — execute immediately.
            # Roman Urdu: READ / WRITE_LOW — foran execute karo.
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
            result_text = json.dumps({
                "success": result.success, "data": result.data,
                "metadata": result.metadata, "error": result.error,
            }, default=str)
            if len(result_text) > 30000:
                result_text = result_text[:30000] + '...[truncated]'
            conversation += (
                f"\n\n[Iteration {iteration}] You called tool '{tool_name}' "
                f"with args {json.dumps(args)}.\nResult:\n{result_text}\n\n"
                f"Now decide: call another tool or produce final_answer."
            )
            continue

        return {
            "answer": "I produced an unexpected reasoning step. Please retry.",
            "tool_calls": tool_calls_log,
            "iterations": iteration,
            "error": f"unknown_action:{action}",
        }

    return {
        "answer": "I reached the maximum reasoning steps.",
        "tool_calls": tool_calls_log,
        "iterations": MAX_ITERATIONS,
        "error": "max_iterations",
        "pending_approval_id": pending_approval_id,
    }
