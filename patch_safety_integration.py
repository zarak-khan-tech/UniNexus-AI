# English: Integrate safety scanning into the reasoning loop.
# Roman Urdu: Reasoning loop mein safety scanning integrate karo.
path = "backend/app/core/reasoning.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Import safety module
old_import = "from backend.app.services.tenant_settings import get_tenant_settings"
new_import = (
    "from backend.app.services.tenant_settings import get_tenant_settings\n"
    "from backend.app.core.safety import scan_request, build_safety_preamble"
)
if old_import not in content:
    print("ERROR: tenant_settings import anchor not found")
    raise SystemExit(1)
content = content.replace(old_import, new_import, 1)

# 2. Scan user request inside reason() and add preamble to conversation
old_setup = """    settings = get_tenant_settings(tenant_id) if tenant_id else {}
    system = _build_system_prompt(settings, tenant_id)
    gw = get_gateway()
    history_block = _format_history(history)
    conversation = (
        f"{history_block}"
        f"User question: {user_request}\\n\\n"
        f"Your turn. Respond with JSON only."
    )"""

new_setup = """    settings = get_tenant_settings(tenant_id) if tenant_id else {}
    system = _build_system_prompt(settings, tenant_id)
    gw = get_gateway()
    history_block = _format_history(history)

    # English: Scan the raw user request for injection attempts.
    # Roman Urdu: Raw user request ko injection attempts ke liye scan karo.
    scan = scan_request(user_request)
    safety_preamble = build_safety_preamble(scan)

    conversation = (
        f"{safety_preamble}"
        f"{history_block}"
        f"User question: {user_request}\\n\\n"
        f"Your turn. Respond with JSON only."
    )"""

if old_setup not in content:
    print("ERROR: reason() setup block not found")
    raise SystemExit(1)
content = content.replace(old_setup, new_setup, 1)

# 3. Add safety flag to the final_answer return
old_final_ret = """            return {
                "answer": answer or "No answer generated.",
                "tool_calls": tool_calls_log, "iterations": iteration,
                "provider": resp.provider, "model": resp.model,
                "pending_approval_id": pending_approval_id,
                "sources": _dedupe_sources(collected_sources),
            }"""

new_final_ret = """            return {
                "answer": answer or "No answer generated.",
                "tool_calls": tool_calls_log, "iterations": iteration,
                "provider": resp.provider, "model": resp.model,
                "pending_approval_id": pending_approval_id,
                "sources": _dedupe_sources(collected_sources),
                "safety": scan,
            }"""

if old_final_ret not in content:
    print("ERROR: final_answer return block not found")
    raise SystemExit(1)
content = content.replace(old_final_ret, new_final_ret, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: reasoning.py integrated with safety scanning")
