"""
English: Wrap tool_registry.call with a 15-second timeout.
Roman Urdu: tool_registry.call ko 15-second timeout ke saath wrap karo.
"""
path = "backend/app/core/reasoning.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add imports
old_import = "from backend.app.tools import tool_registry"
new_import = "from backend.app.tools import tool_registry\nfrom backend.app.core.reliability import run_with_timeout\nfrom backend.app.tools.base import ToolResult"
if "run_with_timeout" not in content:
    if old_import in content:
        content = content.replace(old_import, new_import, 1)
    else:
        print("ERROR: tool_registry import anchor not found")
        raise SystemExit(1)

# 2. Wrap the tool call
old_call = "            result = tool_registry.call(tool_name, **args)"
new_call = """            try:
                # English: Wrap in a 15s timeout to prevent hanging.
                # Roman Urdu: 15s timeout mein wrap karo taake system hang na ho.
                result = run_with_timeout(tool_registry.call, 15.0, tool_name, **args)
            except TimeoutError:
                result = ToolResult(success=False, error="Tool execution timed out after 15 seconds.")"""

if "run_with_timeout(tool_registry.call" in content:
    print("SKIP: tool call already wrapped")
else:
    if old_call in content:
        content = content.replace(old_call, new_call, 1)
    else:
        print("ERROR: tool call line not found")
        raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: reasoning.py wrapped tool calls with 15s timeout")
