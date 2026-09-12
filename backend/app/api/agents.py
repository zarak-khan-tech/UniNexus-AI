from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.agents.orchestrator import OrchestratorAgent
from backend.app.api.deps import get_current_active_user
from backend.app.models.user import User

router = APIRouter(prefix="/agents", tags=["AI Agents"])

class TaskRequest(BaseModel):
    request: str

@router.post("/run")
def run_agent_task(
    task_req: TaskRequest,
    current_user: User = Depends(get_current_active_user)
):
    '''Securely receives a task and asks the Orchestrator to plan it.'''
    orchestrator = OrchestratorAgent()
    result = orchestrator.execute({"request": task_req.request})
    return result
