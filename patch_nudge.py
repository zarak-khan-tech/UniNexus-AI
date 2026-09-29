# English: Add a nudge that forces the LLM to actually CALL a tool instead of
#          describing it in natural language.
# Roman Urdu: Ek nudge add karo jo LLM ko force kare ke tool describe karne ki
#             jagah actually CALL kare.
path = "backend/app/core/reasoning.py"
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()

# Nudge 1: System prompt mein explicit instruction
old_sys = '''HIGH-RISK ACTIONS REQUIRE APPROVAL:'''
new_sys = '''NEVER DESCRIBE A TOOL CALL IN NATURAL LANGUAGE:
- If you decide a tool is needed, you MUST emit {"action": "tool_call", ...}.
- Do NOT write sentences like "we can call X tool" or "the update_student_grade tool will...".
- If you catch yourself describing a tool call, STOP and instead emit the JSON action.

HIGH-RISK ACTIONS REQUIRE APPROVAL:'''

if old_sys not in content:
    print("WARN: system prompt anchor 1 not found; skipping")
else:
    content = content.replace(old_sys, new_sys, 1)
    print("OK: added nudge 1 (system prompt)")

# Nudge 2: Detect description pattern in final_answer and reject it
old_check = '''        if action == "final_answer":
            answer = (decision.get("answer") or "").strip()
            return {'''

new_check = '''        if action == "final_answer":
            answer = (decision.get("answer") or "").strip()

            # English: If the LLM just DESCRIBED a tool call, force a retry with a nudge.
            # Roman Urdu: Agar LLM ne tool call ko sirf DESCRIBE kiya, to nudge ke saath retry karo.
            lowered = answer.lower()
            looks_like_description = any([
                "we can call" in lowered,
                "should call" in lowered,
                "will require human approval" in lowered and "tool" in lowered,
                "call the" in lowered and "tool" in lowered,
            ])
            if looks_like_description and iteration < MAX_ITERATIONS:
                conversation += (
                    "\\n\\n[Correction] Your previous response DESCRIBED a tool call "
                    "instead of emitting an actual tool_call action. "
                    "Do NOT describe. Emit STRICT JSON: "
                    "{{\\"action\\": \\"tool_call\\", \\"tool\\": \\"tool_name\\", \\"args\\": {{...}}}}. "
                    "Try again now."
                )
                continue

            return {'''

if old_check not in content:
    print("WARN: anchor 2 not found; skipping nudge 2")
else:
    content = content.replace(old_check, new_check, 1)
    print("OK: added nudge 2 (description detection)")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("DONE: reasoning.py patched with nudges")
