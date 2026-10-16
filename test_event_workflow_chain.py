"""
English: Verify event -> workflow auto-trigger chain (self-contained).
Roman Urdu: Event -> workflow auto-trigger chain verify karo (self-contained).
"""
import json

from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.models.user import User
from backend.app.models.workflow import Workflow
from backend.app.core.events import event_bus, Event
from backend.app.services.event_triggers import register_event_triggers

# English: Register the bridge in THIS process too.
# Roman Urdu: Is process mein bhi bridge register karo.
register_event_triggers()

db = SessionLocal()
t = db.query(Tenant).first()
u = db.query(User).filter(User.role == 'admin').first()
tid = t.id

db.query(Workflow).filter(Workflow.name == 'Event Fire Test').delete()
db.commit()

wf = Workflow(
    tenant_id=tid,
    user_id=u.id,
    name='Event Fire Test',
    description='Fires when a document is uploaded.',
    trigger_type='event',
    trigger_config_json=json.dumps({'event_type': 'DocumentUploaded'}),
    action_type='notification',
    action_config_json=json.dumps({'message': 'Doc uploaded!'}),
    is_active=True,
)
db.add(wf)
db.commit()
db.refresh(wf)
wf_id = wf.id
db.close()

print(f"Created workflow id={wf_id}, listening for DocumentUploaded")

n = event_bus.publish(Event(
    event_type='DocumentUploaded',
    tenant_id=tid,
    payload={'document_id': 999, 'title': 'Event Fire Test Doc'},
))
print(f"Event published, {n} handler(s) ran")

db = SessionLocal()
wf_after = db.query(Workflow).filter(Workflow.id == wf_id).first()
print(f"run_count: {wf_after.run_count}")
print(f"last_run_at: {wf_after.last_run_at}")

db.query(Workflow).filter(Workflow.id == wf_id).delete()
db.commit()
db.close()

if wf_after.run_count and wf_after.run_count >= 1:
    print("PASS: workflow auto-triggered by event")
else:
    print("FAIL: workflow did not run — check backend logs")
