"""
English: Workflow engine — evaluates triggers and executes actions.
Roman Urdu: Workflow engine — triggers evaluate karta hai aur actions chalata hai.
"""
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from backend.app.core.database import SessionLocal
from backend.app.models.workflow import Workflow
from backend.app.models.student import Student
from backend.app.models.enrollment import Enrollment
from backend.app.services.notifications import create_notification

logger = logging.getLogger(__name__)


def _check_attendance_below(config: Dict[str, Any], tenant_id: int) -> List[Dict[str, Any]]:
    """
    English: Find students whose average attendance is below the threshold.
    Roman Urdu: Students dhoondo jinki average attendance threshold se kam hai.
    """
    threshold = float(config.get('threshold', 60))
    db = SessionLocal()
    try:
        students = db.query(Student).filter(Student.tenant_id == tenant_id).all()
        hits = []
        for s in students:
            enrs = db.query(Enrollment).filter(Enrollment.student_id == s.id).all()
            if not enrs:
                continue
            avg = sum(e.attendance_percentage or 0 for e in enrs) / len(enrs)
            if avg < threshold:
                hits.append({
                    'student_id': s.id,
                    'student_number': s.student_number,
                    'name': f'{s.first_name} {s.last_name}',
                    'average_attendance': round(avg, 1),
                })
        return hits
    finally:
        db.close()


def _execute_action(workflow: Workflow, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    English: Run the action configured on the workflow.
    Roman Urdu: Workflow ka configured action chalao.
    """
    config = json.loads(workflow.action_config_json or '{}')
    action = workflow.action_type

    if action == 'send_notification':
        title = config.get('title', 'Workflow triggered')
        body_template = config.get('body', 'Workflow "{name}" fired with context: {summary}')
        hits = context.get('hits', [])
        summary = f'{len(hits)} student(s) matched' if hits else context.get('summary', 'event happened')
        body = body_template.replace('{name}', workflow.name).replace('{summary}', summary)
        nid = create_notification(
            tenant_id=workflow.tenant_id,
            user_id=workflow.user_id,
            kind='system',
            title=title,
            body=body,
            action_url=config.get('action_url', '/workflows'),
        )
        return {'ok': True, 'notification_id': nid, 'summary': summary}

    if action == 'log_only':
        logger.info(f'[workflow:{workflow.id}] {workflow.name} — {context}')
        return {'ok': True, 'logged': True}

    return {'ok': False, 'error': f'Unknown action: {action}'}


def run_workflow(workflow: Workflow) -> Dict[str, Any]:
    """
    English: Evaluate one workflow; execute its action if the trigger matches.
    Roman Urdu: Ek workflow evaluate karo; trigger match ho to action chalao.
    """
    config = json.loads(workflow.trigger_config_json or '{}')
    trigger = workflow.trigger_type
    context: Dict[str, Any] = {'trigger': trigger}

    if trigger == 'attendance_below':
        hits = _check_attendance_below(config, workflow.tenant_id)
        context['hits'] = hits
        if not hits:
            return {'fired': False, 'reason': 'no students below threshold'}
    elif trigger == 'execution_completed':
        # English: Manual trigger only for now — context supplied by caller.
        # Roman Urdu: Filhaal manual trigger — context caller deta hai.
        context['summary'] = config.get('summary', 'manual run')
    else:
        return {'fired': False, 'reason': f'unknown trigger: {trigger}'}

    result = _execute_action(workflow, context)
    return {'fired': True, 'context': context, 'result': result}


def run_all_active(tenant_id: int) -> List[Dict[str, Any]]:
    """
    English: Evaluate every active workflow for a tenant. Used by the manual "Run all" button.
    Roman Urdu: Tenant ke sab active workflows evaluate karo. Manual "Run all" button ke liye.
    """
    db = SessionLocal()
    try:
        workflows = db.query(Workflow).filter(
            Workflow.tenant_id == tenant_id,
            Workflow.is_active == True,
        ).all()
        out = []
        for w in workflows:
            try:
                r = run_workflow(w)
                w.last_run_at = datetime.utcnow()
                w.run_count = (w.run_count or 0) + 1
                db.commit()
                out.append({'workflow_id': w.id, 'name': w.name, **r})
            except Exception as e:
                logger.error(f'Workflow {w.id} failed: {e}')
                out.append({'workflow_id': w.id, 'name': w.name, 'fired': False, 'error': str(e)})
        return out
    finally:
        db.close()
