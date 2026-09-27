"""
English: Real agentic reasoning loop with strict grounding (no hallucinations).
Roman Urdu: Real agentic reasoning loop with strict grounding.
"""
import json
import logging
from typing import List, Dict, Any
from backend.app.tools import tool_registry
from backend.app.core.llm_gateway import get_gateway

logger = logging.getLogger(__name__)

MAX_ITERATIONS = 5

SYSTEM_PROMPT = """You are the reasoning core of UniNexus AI, a multi-agent 
university intelligence platform.

You have access to TOOLS. To answer:
1. Think about what information you need.
2. Call tools with the right arguments.
3. Look at results. Call more tools if needed.
4. Produce a final answer USING ONLY FACTS FROM THE TOOL RESULTS.

═══════════════════════════════════════════════════════════════
ABSOLUTE RULE — ANTI-HALLUCINATION
═══════════════════════════════════════════════════════════════
- If a fact is NOT in the tool results, DO NOT invent it.
- Do NOT add numbers, dates, fees, or policies that aren't literally 
  in the returned documents.
- If you don't have enough info, say: "I don't have that information 
  in the available documents."
- When stating a policy, QUOTE or closely paraphrase the actual text.
- Always cite the source: "Per the Fee Policy 2026..." or 
  "According to Examination Rules and Regulations..."

EXAMPLES OF WHAT NOT TO DO:
❌ "The fee is PKR 150,000" (if the fee amount is not in the results)
❌ "You may need remedial sessions" (if remedial is not mentioned)
❌ "Re-sits are automatically granted" (unless stated in the source)

EXAMPLES OF WHAT TO DO:
✅ "The Fee Policy 2026 states that fees are set by the Board of 
    Trustees. Specific amounts are published on the finance portal."
✅ "According to the Examination Rules, re-sits are only permitted 
    on documented medical or compassionate grounds."

═══════════════════════════════════════════════════════════════
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

def reason(user_request: str) -> Dict[str, Any]:
    gw = get_gateway()
    tools_desc = _format_tools_for_llm()
    system = SYSTEM_PROMPT.replace("{tools_desc}", tools_desc)

    conversation = f"User question: {user_request}\n\nYour turn. Respond with JSON only."
    tool_calls_log: List[Dict[str, Any]] = []

    for iteration in range(1, MAX_ITERATIONS + 1):
        resp = gw.generate(system + "\n\n" + conversation, json_mode=True)
        if not resp.success or not resp.text:
            logger.warning(f"Reasoning failed at iteration {iteration}: {resp.error}")
            # English: If the LLM call failed, still return whatever we have.
            # Roman Urdu: Agar LLM call fail ho gayi, jo hai wahi return karo.
            if tool_calls_log:
                return {
                    "answer": "I gathered some information but could not finalize the answer. Please try again.",
                    "tool_calls": tool_calls_log,
                    "iterations": iteration,
                    "error": resp.error,
                }
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
                "iteration": iteration,
                "tool": tool_name,
                "args": args,
                "reasoning": reasoning,
                "summary": summary,
            })

            # English: Give the LLM the FULL result so it doesn't have to invent.
            # Roman Urdu: LLM ko poora result do taake usay invent na karna pare.
            result_text = json.dumps({
                "success": result.success,
                "data": result.data,
                "metadata": result.metadata,
                "error": result.error,
            }, default=str)

            # English: Safety cap — Groq handles ~128k, but let's stay tidy.
            # Roman Urdu: Safety cap — Groq 128k handle karta hai, lekin limit rakho.
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
