from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.document import Document
from backend.app.models.agent_execution import AgentExecution
from backend.app.agents.registry import registry

router = APIRouter(prefix='/stats', tags=['Dashboard Statistics'])

@router.get('/overview')
def get_overview(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    '''Returns live dashboard statistics for the current tenant.'''
    tenant_id = current_user.tenant_id

    student_count = db.query(Student).filter(Student.tenant_id == tenant_id).count()
    course_count = db.query(Course).filter(Course.tenant_id == tenant_id).count()
    document_count = db.query(Document).filter(Document.tenant_id == tenant_id).count()
    execution_count = db.query(AgentExecution).filter(AgentExecution.tenant_id == tenant_id).count()

    return {
        'agents': len(registry.list_agents()),
        'students': student_count,
        'courses': course_count,
        'documents': document_count,
        'executions': execution_count,
    }
