"""
English: Test workflows — create one and run it.
Roman Urdu: Workflows test karo — ek banao aur chalao.
"""
from backend.app.core.database import SessionLocal
from backend.app.models.workflow import Workflow
from backend.app.services.workflow_engine import run_all_active
import json

db = SessionLocal()
try:
    # Clean up any existing
    db.query(Workflow).delete()
    db.commit()

    # Create a workflow: if any student has avg attendance below 65% -> notify
    w = Workflow(
        tenant_id=1,
        user_id=1,
        name='Low attendance alert',
        description='Alert admin if any student drops below 65% average attendance',
        trigger_type='attendance_below',
        trigger_config_json=json.dumps({'threshold': 65}),
        action_type='send_notification',
        action_config_json=json.dumps({
            'title': 'Low attendance detected',
            'body': 'Workflow "{name}" triggered: {summary}',
            'action_url': '/students',
        }),
        is_active=True,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    print(f'Created workflow #{w.id}: {w.name}')
finally:
    db.close()

print()
print('Running all active workflows...')
results = run_all_active(tenant_id=1)
for r in results:
    print(json.dumps(r, indent=2, default=str))
