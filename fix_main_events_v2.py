"""
English: Fix main.py — remove duplicate import + add event subscribers after app creation.
Roman Urdu: main.py fix karo — duplicate import hatao + app ke baad event subscribers add karo.
"""
path = "backend/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Remove duplicate "events as events_api"
dup = "imports, documents, search, events as events_api, events as events_api"
single = "imports, documents, search, events as events_api"
if dup in content:
    content = content.replace(dup, single, 1)
    print("FIXED: duplicate 'events as events_api' import removed")
else:
    print("SKIP: no duplicate import found")

# Fix 2: Add demo subscriber + logging setup right after FastAPI app creation
if "event_bus.subscribe" in content:
    print("SKIP: subscribers already present")
else:
    anchor = "app.add_middleware(\n    CORSMiddleware,"
    addition = """import logging

# English: Event bus demo subscriber setup.
# Roman Urdu: Event bus demo subscriber setup.
_logger = logging.getLogger("uninexus.events")


def _log_event(e):
    _logger.info(f"[event] {e.event_type} tenant={e.tenant_id} payload_keys={list(e.payload.keys())}")


from backend.app.core.events import event_bus  # noqa: E402
event_bus.subscribe("DocumentUploaded", _log_event)
event_bus.subscribe("StudentImported", _log_event)


app.add_middleware(
    CORSMiddleware,"""
    if anchor not in content:
        print("ERROR: middleware anchor not found")
    else:
        content = content.replace(anchor, addition, 1)
        print("FIXED: demo subscribers added")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
