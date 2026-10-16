# English: Make audit log rows clickable and navigate to detail page.
# Roman Urdu: Audit log rows clickable banao aur detail page pe navigate.
path = "src/pages/AuditLogs.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add useNavigate import
old_import = "import { useEffect, useState } from 'react';"
new_import = "import { useEffect, useState } from 'react';\nimport { useNavigate } from 'react-router-dom';"
if old_import not in content:
    print("ERROR: react import anchor not found")
    raise SystemExit(1)
content = content.replace(old_import, new_import, 1)

# 2. Add navigate hook inside component
old_hook = "  const [executions, setExecutions] = useState([]);"
new_hook = "  const navigate = useNavigate();\n  const [executions, setExecutions] = useState([]);"
if old_hook not in content:
    print("ERROR: executions state not found")
    raise SystemExit(1)
content = content.replace(old_hook, new_hook, 1)

# 3. Add onClick + cursor-pointer to table row
old_row = '<tr key={row.id} className="border-t border-ink-100 hover:bg-ink-50/40 transition-colors">'
new_row = '<tr key={row.id} onClick={() => navigate(`/audit/${row.id}`)} className="border-t border-ink-100 hover:bg-ink-50/40 transition-colors cursor-pointer">'
if old_row not in content:
    print("ERROR: table row anchor not found")
    raise SystemExit(1)
content = content.replace(old_row, new_row, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: AuditLogs.jsx rows now navigate to /audit/{id}")
