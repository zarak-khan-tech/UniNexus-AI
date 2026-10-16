"""
English: Add an 'event' trigger branch to run_workflow. Event-triggered workflows
skip attendance/execution checks — the event_triggers bridge already matched them.
Roman Urdu: run_workflow mein 'event' trigger branch add karo. Event-triggered
workflows attendance/execution checks skip karte hain — event_triggers bridge
already match kar chuka hota hai.
"""
path = "backend/app/services/workflow_engine.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if "trigger == 'event'" in content:
    print("SKIP: 'event' branch already present")
    raise SystemExit(0)

# Insert the 'event' branch right after the 'execution_completed' branch
old = """    elif trigger == 'execution_completed':
        # English: Manual trigger only for now — context supplied by caller.
        # Roman Urdu: Filhaal manual trigger — context caller deta hai.
        context['summary'] = config.get('summary', 'manual run')
    else:"""

new = """    elif trigger == 'execution_completed':
        # English: Manual trigger only for now — context supplied by caller.
        # Roman Urdu: Filhaal manual trigger — context caller deta hai.
        context['summary'] = config.get('summary', 'manual run')
    elif trigger == 'event':
        # English: Event-triggered. The event_triggers bridge already matched
        # the event against config['event_type']; here we just pass the payload
        # through to the action.
        # Roman Urdu: Event-triggered. event_triggers bridge already event ko
        # config['event_type'] se match kar chuka hai; yahan hum sirf payload
        # action ko pass kar rahe hain.
        context['event'] = config.get('event_payload', {})
    else:"""

if old not in content:
    print("ERROR: 'execution_completed' branch anchor not found")
    raise SystemExit(1)

content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: 'event' trigger branch added to workflow_engine.py")
