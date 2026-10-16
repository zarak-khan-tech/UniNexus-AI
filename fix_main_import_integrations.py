"""
English: Ensure main.py imports the integrations package so adapters self-register.
Roman Urdu: main.py integrations package import kare taake adapters self-register hon.
"""
path = "backend/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add explicit package import if not present
if "from backend.app import integrations" in content:
    print("SKIP: package import already present")
else:
    anchor = "from backend.app.api import auth, agents"
    if anchor not in content:
        print("ERROR: api import anchor not found")
        raise SystemExit(1)
    content = content.replace(
        anchor,
        "from backend.app import integrations  # noqa: F401  (triggers adapter registration)\n" + anchor,
        1,
    )
    print("FIXED: integrations package imported")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
