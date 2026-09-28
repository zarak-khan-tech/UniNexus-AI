"""
English: API routes for agents, reasoning, and LLM provider management.
Roman Urdu: Agents, reasoning, aur LLM provider management ke API routes.
"""
import json
import time
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.agents.orchestrator import OrchestratorAgent
from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.core.llm import check_ollama_status
from backend.app.core.llm_gateway import get_gateway
from backend.app.core.reasoning import reason as reasoning_loop
from backend.app.models.user import User
from backend.app.models.agent_execution import AgentExecution

registry.register(AttendanceAgent())
registry.register(PolicyAgent())
registry.register(RiskAgent())
registry.register(KnowledgeAgent())

router = APIRouter(prefix='/agents', tags=['AI Agents'])


class HistoryTurn(BaseModel):
    role: str
    content: str


class TaskRequest(BaseModel):
    request: str


class ReasoningRequest(BaseModel):
    request: str
    history: Optional[List[HistoryTurn]] = None


class ProviderSwitchRequest(BaseModel):
    provider: str


@router.post('/run')
def run_agent_task(
    task_req: TaskRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    start = time.time()
    orchestrator = OrchestratorAgent()
    result = orchestrator.execute({'request': task_req.request})
    duration_ms = (time.time() - start) * 1000

    execution = AgentExecution(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        user_email=current_user.email,
        original_request=result['original_request'],
        status=result['status'],
        execution_plan_json=json.dumps(result.get('execution_plan', [])),
        execution_results_json=json.dumps(result.get('execution_results', [])),
        duration_ms=duration_ms,
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    result['execution_id'] = execution.id
    result['duration_ms'] = round(duration_ms, 2)
    return result


@router.post('/reason')
def run_reasoning(
    task_req: ReasoningRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    start = time.time()
    history_dicts = [h.dict() for h in (task_req.history or [])]
    result = reasoning_loop(task_req.request, history=history_dicts)
    duration_ms = (time.time() - start) * 1000

    execution = AgentExecution(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        user_email=current_user.email,
        original_request=task_req.request,
        status='completed' if not result.get('error') else 'partial',
        execution_plan_json=json.dumps(result.get('tool_calls', [])),
        execution_results_json=json.dumps({'answer': result.get('answer')}),
        duration_ms=duration_ms,
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    return {
        'mode': 'agentic_reasoning',
        'original_request': task_req.request,
        'answer': result.get('answer'),
        'tool_calls': result.get('tool_calls', []),
        'iterations': result.get('iterations', 0),
        'provider': result.get('provider'),
        'model': result.get('model'),
        'execution_id': execution.id,
        'duration_ms': round(duration_ms, 2),
        'status': 'completed' if not result.get('error') else 'partial',
    }


@router.get('/list')
def list_registered_agents(current_user: User = Depends(get_current_active_user)):
    return {'agents': registry.list_agents()}


@router.get('/executions')
def list_executions(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(AgentExecution)
        .filter(AgentExecution.tenant_id == current_user.tenant_id)
        .order_by(AgentExecution.created_at.desc())
        .limit(limit)
        .all()
    )
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
        ],
    }


@router.get('/llm/status')
def llm_status(current_user: User = Depends(get_current_active_user)):
    return check_ollama_status()


@router.post('/llm/provider')
def switch_llm_provider(
    body: ProviderSwitchRequest,
    current_user: User = Depends(get_current_active_user),
):
    gateway = get_gateway()
    ok = gateway.set_primary(body.provider)
    if not ok:
        raise HTTPException(status_code=400, detail=f'Unknown provider: {body.provider}')
    return {
        'ok': True,
        'primary_provider': gateway.primary_name,
        'status': check_ollama_status(),
    }
