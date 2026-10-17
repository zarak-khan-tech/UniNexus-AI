"""
English: Diagnostic — print what the bridge sees and why the workflow
doesn't fire.
Roman Urdu: Diagnostic — bridge kya dekhta hai aur workflow kyun fire nahi
hota, print karo.
"""
import json
import logging

# Force INFO logs to show
logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(name)s | %(message)s')

from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.models.user import User
from backend.app.models.workflow import Workflow

db = SessionLocal()
t = db.query(Tenant).first()
u = db.query(User).filter(User.role == 'admin').first()
tid = t.id
print(f"Tenant id: {tid}")

db.query(Workflow).filter(Workflow.name == 'Event Fire Test Diag').delete()
db.commit()

wf = Workflow(
    tenant_id=tid,
    user_id=u.id,
    name='Event Fire Test Diag',
    description='diag',
    trigger_type='event',
    trigger_config_json=json.dumps({'event_type': 'DocumentUploaded'}),
    action_type='notification',
    action_config_json=json.dumps({'message': 'x'}),
    is_active=True,
)
db.add(wf)
db.commit()
db.refresh(wf)
wf_id = wf.id
print(f"Created wf id={wf_id}")
print(f"  tenant_id={wf.tenant_id}")
print(f"  trigger_type={wf.trigger_type}")
print(f"  trigger_config_json={wf.trigger_config_json}")
print(f"  is_active={wf.is_active}")
db.close()

# Now simulate what the bridge does
from backend.app.core.events import Event
event = Event(event_type='DocumentUploaded', tenant_id=tid, payload={'k':'v'})

db = SessionLocal()
try:
    wfs = (
        db.query(Workflow)
        .filter(
            Workflow.tenant_id == event.tenant_id,
            Workflow.is_active == True,  # noqa
            Workflow.trigger_type == 'event',
        )
        .all()
    )
    print(f"\nQuery matched {len(wfs)} workflow(s)")
    for w in wfs:
        print(f"  - id={w.id} name={w.name}")
        cfg = json.loads(w.trigger_config_json or '{}')
        print(f"    cfg={cfg}")
        print(f"    cfg.event_type={cfg.get('event_type')!r}")
        print(f"    event.event_type={event.event_type!r}")
        print(f"    match={cfg.get('event_type') == event.event_type}")

        # Try running it
        from backend.app.services.workflow_engine import run_workflow
        try:
            result = run_workflow(w)
            print(f"    run_workflow result: {result}")
            print(f"    after: run_count={w.run_count} last_run_at={w.last_run_at}")
        except Exception as e:
            import traceback
            print(f"    EXCEPTION: {e}")
            traceback.print_exc()
finally:
    db.query(Workflow).filter(Workflow.name == 'Event Fire Test Diag').delete()
    db.commit()
    db.close()
