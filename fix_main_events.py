"""
English: Fix main.py — remove duplicate events_api.router + add demo subscribers.
Roman Urdu: main.py fix karo — duplicate events_api.router hatao + demo subscribers add karo.
"""
path = "backend/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Remove duplicate events_api.router line
dup = "app.include_router(events_api.router)\napp.include_router(events_api.router)"
single = "app.include_router(events_api.router)"
if dup in content:
    content = content.replace(dup, single, 1)
    print("FIXED: duplicate events_api.router removed")
else:
    # Try the CRLF variant
    dup_crlf = "app.include_router(events_api.router)\r\napp.include_router(events_api.router)"
    if dup_crlf in content:
        content = content.replace(dup_crlf, single, 1)
        print("FIXED: duplicate events_api.router removed (CRLF)")
    else:
        print("SKIP: no duplicate events_api.router found")

# Fix 2: Add demo subscriber if missing
if "event_bus.subscribe" in content:
    print("SKIP: subscribers already present")
else:
    anchor = "logger = logging.getLogger(__name__)"
    if anchor not in content:
        print("ERROR: logger anchor not found — paste main.py head lines")
    else:
        addition = anchor + """

# English: Register a demo subscriber for the event bus on module load.
# Roman Urdu: Module load pe event bus ke liye ek demo subscriber register karo.
def _log_event(e):
    logger.info(f"[event] {e.event_type} tenant={e.tenant_id} payload_keys={list(e.payload.keys())}")

from backend.app.core.events import event_bus  # noqa: E402
event_bus.subscribe('DocumentUploaded', _log_event)
event_bus.subscribe('StudentImported', _log_event)"""
        content = content.replace(anchor, addition, 1)
        print("FIXED: demo subscribers added")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
