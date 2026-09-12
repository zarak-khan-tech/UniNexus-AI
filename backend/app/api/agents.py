import json
import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.agents.orchestrator import OrchestratorAgent
from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.agent_execution import AgentExecution

# Register agents globally
registry.register(AttendanceAgent())
registry.register(PolicyAgent())
registry.register(RiskAgent())
registry.register(KnowledgeAgent())

router = APIRouter(prefix='/agents', tags=['AI Agents'])

class TaskRequest(BaseModel):
    request: str

@router.post('/run')
def run_agent_task(
    task_req: TaskRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    '''Securely receives a task, executes it, and logs it for audit.'''
    start = time.time()
    orchestrator = OrchestratorAgent()
    result = orchestrator.execute({'request': task_req.request})
    duration_ms = (time.time() - start) * 1000

    # Persist audit record
    execution = AgentExecution(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        user_email=current_user.email,
        original_request=result['original_request'],
        status=result['status'],
        execution_plan_json=json.dumps(result['execution_plan']),
        execution_results_json=json.dumps(result['execution_results']),
        duration_ms=duration_ms
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    # Add execution id to response
    result['execution_id'] = execution.id
    result['duration_ms'] = round(duration_ms, 2)
    return result

@router.get('/list')
def list_registered_agents(current_user: User = Depends(get_current_active_user)):
    return {'agents': registry.list_agents()}

@router.get('/executions')
def list_executions(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    '''Returns recent agent executions for the current tenant (audit log).'''
    rows = db.query(AgentExecution)\
        .filter(AgentExecution.tenant_id == current_user.tenant_id)\
        .order_by(AgentExecution.created_at.desc())\
        .limit(limit).all()

    return {
        'total': len(rows),
        'executions': [
            {
                'id': r.id,
                'user_email': r.user_email,
                'original_request': r.original_request,
                'status': r.status,
                'duration_ms': r.duration_ms,
                'created_at': r.created_at.isoformat(),
            }
            for r in rows
        ]
    }
