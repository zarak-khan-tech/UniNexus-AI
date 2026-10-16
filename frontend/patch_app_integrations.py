"""
English: Add /integrations route to App.jsx.
Roman Urdu: /integrations route App.jsx mein add karo.
"""
path = "src/App.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import
if "import Integrations from" in content:
    print("SKIP: import already present")
else:
    anchor = "import SearchBox from './components/SearchBox';"
    if anchor not in content:
        # Fallback: try a common import
        anchor = "import AuditLogs from './pages/AuditLogs';"
        if anchor not in content:
            print("ERROR: import anchor not found — paste App.jsx head lines")
            raise SystemExit(1)
    content = content.replace(
        anchor,
        anchor + "\nimport Integrations from './pages/Integrations';",
        1,
    )
    print("FIXED: Integrations import added")

# 2. Add route — after /tools or /agents route
if "/integrations" in content:
    print("SKIP: route already present")
else:
    # Try common anchors
    anchors = [
        '<Route path="/tools"',
        '<Route path="/agents"',
        '<Route path="/settings"',
    ]
    target = None
    for a in anchors:
        if a in content:
            target = a
            break
    if not target:
        print("ERROR: route anchor not found — paste App.jsx routes section")
        raise SystemExit(1)

    # Find the full route line and insert after it
    import re
    pattern = re.compile(
        r"(<Route path=\"(?:/tools|/agents|/settings)\"[^\n]*?/>)",
        re.DOTALL,
    )
    match = pattern.search(content)
    if not match:
        print("ERROR: could not match route line")
        raise SystemExit(1)

    line = match.group(1)
    new_route = line + '\n        <Route path="/integrations" element={<Integrations />} />'
    content = content.replace(line, new_route, 1)
    print("FIXED: /integrations route added")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
