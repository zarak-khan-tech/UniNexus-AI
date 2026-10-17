"""
English: Register event triggers on startup.
Roman Urdu: Startup pe event triggers register karo.
"""
path = "backend/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if "register_event_triggers" in content:
    print("SKIP: event triggers already wired")
    raise SystemExit(0)

# Add import
anchor_imp = "from backend.app.core.events import event_bus"
if anchor_imp not in content:
    print("ERROR: event_bus import anchor not found")
    raise SystemExit(1)
content = content.replace(
    anchor_imp,
    anchor_imp + "\nfrom backend.app.services.event_triggers import register_event_triggers",
    1,
)

# Call inside the startup handler (after existing lines)
anchor_startup = "Base.metadata.create_all(bind=engine)"
if anchor_startup not in content:
    print("ERROR: startup anchor not found")
    raise SystemExit(1)
content = content.replace(
    anchor_startup,
    anchor_startup + "\n    register_event_triggers()",
    1,
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: event triggers wired into startup")
