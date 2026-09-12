from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.agents.orchestrator import OrchestratorAgent
from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent
from backend.app.api.deps import get_current_active_user
from backend.app.models.user import User

# Register agents globally
registry.register(AttendanceAgent())
registry.register(PolicyAgent())
registry.register(RiskAgent())

router = APIRouter(prefix="/agents", tags=["AI Agents"])

class TaskRequest(BaseModel):
    request: str

@router.post("/run")
def run_agent_task(
    task_req: TaskRequest,
    current_user: User = Depends(get_current_active_user)
):
    '''Securely receives a task and asks the Orchestrator to plan and execute it.'''
    orchestrator = OrchestratorAgent()
    result = orchestrator.execute({"request": task_req.request})
    return result

@router.get("/list")
def list_registered_agents(current_user: User = Depends(get_current_active_user)):
    '''Lists all agents currently registered in the system.'''
    return {"agents": registry.list_agents()}
