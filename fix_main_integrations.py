"""
English: Register integrations router in main.py.
Roman Urdu: integrations router ko main.py mein register karo.
"""
path = "backend/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import
old_imp = "imports, documents, search, events as events_api"
new_imp = "imports, documents, search, events as events_api, integrations"
if new_imp in content:
    print("SKIP: import already present")
else:
    if old_imp not in content:
        print("ERROR: api import anchor not found")
        raise SystemExit(1)
    content = content.replace(old_imp, new_imp, 1)
    print("FIXED: integrations import added")

# 2. Register router
if "app.include_router(integrations.router)" in content:
    print("SKIP: router already registered")
else:
    anchor = "app.include_router(events_api.router)"
    if anchor not in content:
        print("ERROR: events_api.router anchor not found")
        raise SystemExit(1)
    content = content.replace(
        anchor,
        anchor + "\napp.include_router(integrations.router)",
        1,
    )
    print("FIXED: integrations router registered")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
