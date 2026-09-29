"""
English: Approvals API — list, approve, reject pending high-risk actions.
Roman Urdu: Approvals API — pending high-risk actions list/approve/reject.
"""
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.approval import Approval
from backend.app.tools import tool_registry
from backend.app.services.notifications import create_notification

router = APIRouter(prefix='/approvals', tags=['Approvals'])


@router.get('')
def list_approvals(
    status: str = 'pending',
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    q = db.query(Approval).filter(Approval.tenant_id == current_user.tenant_id)
    if status != 'all':
        q = q.filter(Approval.status == status)
    rows = q.order_by(Approval.created_at.desc()).limit(100).all()
    return {
        'total': len(rows),
        'approvals': [
            {
                'id': r.id,
                'user_email': r.user_email,
                'tool_name': r.tool_name,
                'args': json.loads(r.args_json) if r.args_json else {},
                'action_description': r.action_description,
                'reasoning': r.reasoning,
                'status': r.status,
                'result': json.loads(r.result_json) if r.result_json else None,
                'error': r.error,
                'created_at': r.created_at.isoformat(),
                'resolved_at': r.resolved_at.isoformat() if r.resolved_at else None,
                'resolved_by_email': r.resolved_by_email,
            }
            for r in rows
        ],
    }


@router.post('/{approval_id}/approve')
def approve(
    approval_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    a = db.query(Approval).filter(
        Approval.id == approval_id,
        Approval.tenant_id == current_user.tenant_id,
    ).first()
    if not a:
        raise HTTPException(status_code=404, detail='Approval not found')
    if a.status != 'pending':
        raise HTTPException(status_code=400, detail=f'Approval already {a.status}')

    args = json.loads(a.args_json) if a.args_json else {}
    result = tool_registry.call(a.tool_name, **args)

    a.status = 'executed' if result.success else 'failed'
    a.result_json = json.dumps(result.data) if result.data else None
    a.error = result.error
    a.resolved_at = datetime.utcnow()
    a.resolved_by_email = current_user.email
    db.commit()

    try:
        if a.user_id and a.user_id != current_user.id:
            create_notification(
                tenant_id=a.tenant_id,
                user_id=a.user_id,
                kind='approval',
                title='Your approval was granted',
                body=f'{a.tool_name.replace("_", " ").title()} was approved by {current_user.email}.',
                action_url='/approvals',
            )
    except Exception:
        pass

    return {
        'ok': result.success,
        'status': a.status,
        'result': result.data,
        'error': result.error,
    }


@router.post('/{approval_id}/reject')
def reject(
    approval_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    a = db.query(Approval).filter(
        Approval.id == approval_id,
        Approval.tenant_id == current_user.tenant_id,
    ).first()
    if not a:
        raise HTTPException(status_code=404, detail='Approval not found')
    if a.status != 'pending':
        raise HTTPException(status_code=400, detail=f'Approval already {a.status}')

    a.status = 'rejected'
    a.resolved_at = datetime.utcnow()
    a.resolved_by_email = current_user.email
    db.commit()

    try:
        if a.user_id and a.user_id != current_user.id:
            create_notification(
                tenant_id=a.tenant_id,
                user_id=a.user_id,
                kind='approval',
                title='Your approval was declined',
                body=f'{a.tool_name.replace("_", " ").title()} was declined by {current_user.email}.',
                action_url='/approvals',
            )
    except Exception:
        pass

    return {'ok': True, 'status': 'rejected'}
