"""
English: API routes for agents, reasoning, LLM provider, and agent definitions.
Roman Urdu: Agents, reasoning, LLM provider, aur agent definitions ke API routes.
"""
import json
import time
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.agents.orchestrator import OrchestratorAgent
from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent
from backend.app.api.deps import get_current_active_user
from backend.app.api.roles import require_role, ADMIN_ROLES
from backend.app.core.database import get_db
from backend.app.core.llm import check_ollama_status
from backend.app.core.llm_gateway import get_gateway
from backend.app.core.reasoning import reason as reasoning_loop
from backend.app.core.rate_limit import rate_limiter
from backend.app.services.agent_definitions import list_agent_definitions, update_agent_definition
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


class AgentDefinitionUpdate(BaseModel):
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    supported_tools: Optional[List[str]] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None


@router.post('/run')
def run_agent_task(
    task_req: TaskRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # English: Per-user rate limit — 30 requests / 60s by default.
    # Roman Urdu: Per-user rate limit — 30 requests / 60s default.
    allowed, retry_after = rate_limiter.check(current_user.email)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )

    start = time.time()
    orchestrator = OrchestratorAgent()
    result = orchestrator.execute({
        'request': task_req.request,
        'tenant_id': current_user.tenant_id,
    })
    duration_ms = (time.time() - start) * 1000

    execution = AgentExecution(
        tenant_id=current_user.tenant_id, user_id=current_user.id,
        user_email=current_user.email, original_request=result['original_request'],
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
    # English: Per-user rate limit — same bucket as /agents/run.
    # Roman Urdu: Per-user rate limit — /agents/run wala same bucket.
    allowed, retry_after = rate_limiter.check(current_user.email)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )

    start = time.time()
    history_dicts = [h.dict() for h in (task_req.history or [])]
    result = reasoning_loop(
        task_req.request,
        history=history_dicts,
        user_id=current_user.id,
        user_email=current_user.email,
        tenant_id=current_user.tenant_id,
    )
    duration_ms = (time.time() - start) * 1000

    execution = AgentExecution(
        tenant_id=current_user.tenant_id, user_id=current_user.id,
        user_email=current_user.email, original_request=task_req.request,
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
        # English: Deduped RAG sources for the frontend.
        # Roman Urdu: Frontend ke liye deduped RAG sources.
        'sources': result.get('sources', []),
    }


@router.get('/list')
def list_registered_agents(
    include_inactive: bool = True,
    current_user: User = Depends(get_current_active_user),
):
    # English: Return all agents by default so the UI can show disabled ones
    #          with a "Paused" state. Callers can pass ?include_inactive=false
    #          to filter to only active.
    # Roman Urdu: Default mein saare agents return karo taake UI disabled ko
    #             "Paused" state mein dikha sake. Filter ke liye
    #             ?include_inactive=false pass karo.
    return {'agents': list_agent_definitions(current_user.tenant_id, active_only=not include_inactive)}


@router.patch('/definitions/{agent_name}')
def patch_agent_definition(
    agent_name: str,
    body: AgentDefinitionUpdate,
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
):
    updates = {k: v for k, v in body.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail='No fields to update')
    row = update_agent_definition(current_user.tenant_id, agent_name, updates)
    if not row:
        raise HTTPException(status_code=404, detail=f'Agent definition not found: {agent_name}')
    return {'ok': True, 'definition': row}


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
        .limit(limit).all()
    )
    return {
        'total': len(rows),
        'executions': [
            {
                'id': r.id, 'user_email': r.user_email,
                'original_request': r.original_request,
                'status': r.status, 'duration_ms': r.duration_ms,
                'created_at': r.created_at.isoformat(),
            } for r in rows
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
        'ok': True, 'primary_provider': gateway.primary_name,
        'status': check_ollama_status(),
    }

@router.get('/executions/{execution_id}')
def get_execution_detail(
    execution_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    English: Return full detail for a single execution (plan, results, 
    duration, sources, safety).
    Roman Urdu: Ek single execution ki poori detail return karo (plan, 
    results, duration, sources, safety).
    """
    row = db.query(AgentExecution).filter(
        AgentExecution.id == execution_id,
        AgentExecution.tenant_id == current_user.tenant_id,
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail='Execution not found')

    try:
        plan = json.loads(row.execution_plan_json or '[]')
    except Exception:
        plan = []
    try:
        results = json.loads(row.execution_results_json or '[]')
    except Exception:
        results = {}

    return {
        'id': row.id,
        'tenant_id': row.tenant_id,
        'user_email': row.user_email,
        'original_request': row.original_request,
        'status': row.status,
        'duration_ms': row.duration_ms,
        'created_at': row.created_at.isoformat(),
        'execution_plan': plan,
        'execution_results': results,
    }

