"""
English: Workflows API — CRUD + manual run.
Roman Urdu: Workflows API — CRUD + manual run.
"""
import json
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.workflow import Workflow
from backend.app.services.workflow_engine import run_workflow, run_all_active

router = APIRouter(prefix='/workflows', tags=['Workflows'])


class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = ''
    trigger_type: str
    trigger_config: Optional[dict] = {}
    action_type: str
    action_config: Optional[dict] = {}


@router.get('')
def list_workflows(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    rows = db.query(Workflow).filter(
        Workflow.tenant_id == current_user.tenant_id,
    ).order_by(Workflow.created_at.desc()).all()
    return {
        'total': len(rows),
        'workflows': [
            {
                'id': w.id,
                'name': w.name,
                'description': w.description,
                'trigger_type': w.trigger_type,
                'trigger_config': json.loads(w.trigger_config_json or '{}'),
                'action_type': w.action_type,
                'action_config': json.loads(w.action_config_json or '{}'),
                'is_active': w.is_active,
                'run_count': w.run_count,
                'last_run_at': w.last_run_at.isoformat() if w.last_run_at else None,
                'created_at': w.created_at.isoformat(),
            }
            for w in rows
        ],
    }


@router.post('')
def create_workflow(
    body: WorkflowCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    w = Workflow(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        name=body.name,
        description=body.description or '',
        trigger_type=body.trigger_type,
        trigger_config_json=json.dumps(body.trigger_config or {}),
        action_type=body.action_type,
        action_config_json=json.dumps(body.action_config or {}),
        is_active=True,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return {'id': w.id, 'ok': True}


@router.post('/{workflow_id}/toggle')
def toggle_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    w = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.tenant_id == current_user.tenant_id,
    ).first()
    if not w:
        raise HTTPException(status_code=404, detail='Workflow not found')
    w.is_active = not w.is_active
    db.commit()
    return {'ok': True, 'is_active': w.is_active}


@router.post('/{workflow_id}/run')
def run_one(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    w = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.tenant_id == current_user.tenant_id,
    ).first()
    if not w:
        raise HTTPException(status_code=404, detail='Workflow not found')
    result = run_workflow(w)
    w.last_run_at = datetime.utcnow()
    w.run_count = (w.run_count or 0) + 1
    db.commit()
    return result


@router.post('/run-all')
def run_all(
    current_user: User = Depends(get_current_active_user),
):
    return {'results': run_all_active(current_user.tenant_id)}


@router.delete('/{workflow_id}')
def delete_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    w = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.tenant_id == current_user.tenant_id,
    ).first()
    if not w:
        raise HTTPException(status_code=404, detail='Workflow not found')
    db.delete(w)
    db.commit()
    return {'ok': True}
