"""
English: Real agentic reasoning loop with session memory and strict tool-calling.
Roman Urdu: Real agentic reasoning loop with session memory aur strict tool-calling.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from backend.app.tools import tool_registry
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

═══════════════════════════════════════════════════════════════
CRITICAL RULE — ALWAYS CALL A TOOL WHEN THE USER ASKS ABOUT DATA
═══════════════════════════════════════════════════════════════
If the user asks for ACTUAL DATA — students, attendance, grades, courses, enrollments, risks — you MUST call a tool.
NEVER say "I don't have that information" without first trying a tool.
Phrases that REQUIRE a tool call:
- "show me students..." → attendance_query or list_students
- "which students..." / "who is..." → attendance_query or list_enrollments
- "find students..." → student_lookup or attendance_query
- "list students..." → list_students
- "which might fail" / "at risk" → list_enrollments
- "what does the policy say" / "rules about" → semantic_search
- "what is the definition of X" / "what counts as X" / "is X passing" -> semantic_search FIRST
- "what grade is passing" / "minimum CGPA" / "pass/fail criteria" -> semantic_search FIRST

IMPORTANT: When the user asks a question that needs a DEFINITION or POLICY
(passing grade, minimum CGPA, attendance threshold, etc.), you MUST first
call semantic_search to look it up. Do NOT say "not found in available data"
without first searching the university documents with semantic_search.

Only skip tools for pure greetings ("hello", "how are you") or meta questions about YOU ("what are you").

═══════════════════════════════════════════════════════════════
ANTI-HALLUCINATION
═══════════════════════════════════════════════════════════════
- If a fact is NOT in the tool results, DO NOT invent it.
- Do NOT add numbers, dates, fees, or policies not in the returned documents.
- When stating a policy, QUOTE or closely paraphrase the actual text.
- Always cite the source: "Per the Fee Policy 2026..." or "According to Attendance Policy 2026..."

Available tools:
{tools_desc}

Respond with STRICT JSON in one of these two shapes:

A) To call a tool:
{{"action": "tool_call", "tool": "tool_name", "args": {{...}}, "reasoning": "why"}}

B) When ready to answer:
{{"action": "final_answer", "answer": "your grounded answer, citing sources"}}

Remember: when in doubt, CALL A TOOL. The user is here to get real data.
"""

def _format_tools_for_llm() -> str:
    lines = []
    for t in tool_registry.list():
        args = t.get('input_schema', {}).get('properties', {})
        arg_str = ', '.join([f"{k}: {v.get('type', 'any')}" for k, v in args.items()]) or 'no args'
        lines.append(f"- {t['name']}: {t['description']} | args: {arg_str}")
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

def reason(user_request: str, history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
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
            logger.error(f"Bad JSON from LLM: {e}. Raw: {raw[:200]}")
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
            }

        if action == "tool_call":
            tool_name = decision.get("tool")
            args = decision.get("args") or {}
            reasoning = decision.get("reasoning", "")
            logger.info(f"[iter {iteration}] Tool call: {tool_name} | {reasoning}")
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
                f"Now decide: call another tool or produce final_answer. "
                f"Remember: DO NOT invent anything not in the results above."
            )
            continue

        logger.warning(f"Unknown action: {action}")
        return {
            "answer": "I produced an unexpected reasoning step. Please retry.",
            "tool_calls": tool_calls_log,
            "iterations": iteration,
            "error": f"unknown_action:{action}",
        }

    return {
        "answer": "I reached the maximum reasoning steps. Here's what I found so far.",
        "tool_calls": tool_calls_log,
        "iterations": MAX_ITERATIONS,
        "error": "max_iterations",
    }
