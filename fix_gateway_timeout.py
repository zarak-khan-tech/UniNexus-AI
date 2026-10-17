"""
English: Add a 20s timeout to each LLM provider call in the gateway.
Roman Urdu: Gateway mein har LLM provider call ke liye 20s timeout add karo.
"""
path = "backend/app/core/llm_gateway/gateway.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import for run_with_timeout
old_import = "from backend.app.core.llm_gateway.base import LLMResponse"
new_import = "from backend.app.core.llm_gateway.base import LLMResponse\nfrom backend.app.core.reliability import run_with_timeout"

if "run_with_timeout" not in content:
    if old_import in content:
        content = content.replace(old_import, new_import, 1)
    else:
        print("ERROR: LLMResponse import anchor not found")
        raise SystemExit(1)

# 2. Wrap provider.generate
old_call = "            resp = provider.generate(prompt, json_mode=json_mode)"
new_call = """            try:
                # English: Wrap the LLM call in a 20s timeout.
                # Roman Urdu: LLM call ko 20s timeout mein wrap karo.
                resp = run_with_timeout(provider.generate, 20.0, prompt, json_mode=json_mode)
            except TimeoutError:
                resp = LLMResponse(
                    text="", provider=name, model="timeout",
                    success=False, error="Provider timed out after 20 seconds."
                )"""

if "run_with_timeout(provider.generate" in content:
    print("SKIP: provider.generate already wrapped")
else:
    if old_call in content:
        content = content.replace(old_call, new_call, 1)
    else:
        print("ERROR: provider.generate line not found")
        raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: Added 20s timeout to LLM gateway provider calls")
