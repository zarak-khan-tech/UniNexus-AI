# English: Register the new /documents router in main.py.
# Roman Urdu: Naya /documents router main.py mein register karo.
path = "backend/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_import = "from backend.app.api import auth, agents, stats, academic, analytics, approvals, tools, notifications, workflows, tenant as tenant_api, imports"
new_import = "from backend.app.api import auth, agents, stats, academic, analytics, approvals, tools, notifications, workflows, tenant as tenant_api, imports, documents"
if old_import not in content:
    print("ERROR: api import anchor not found")
    raise SystemExit(1)
content = content.replace(old_import, new_import, 1)

old_inc = "app.include_router(imports.router)"
new_inc = "app.include_router(imports.router)\napp.include_router(documents.router)"
if old_inc not in content:
    print("ERROR: imports include anchor not found")
    raise SystemExit(1)
content = content.replace(old_inc, new_inc, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: main.py registered documents router")
