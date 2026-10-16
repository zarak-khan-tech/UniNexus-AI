"""
English: Global search API — searches students, courses, documents, agents, 
and tools within the current tenant.
Roman Urdu: Global search API — current tenant ke andar students, courses, 
documents, agents, aur tools search karta hai.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.document import Document
from backend.app.agents.registry import registry
from backend.app.tools import tool_registry

router = APIRouter(prefix='/search', tags=['Search'])

LIMIT_PER_CATEGORY = 5


@router.get('')
def global_search(
    q: str = Query(..., min_length=2),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    English: Search across all major entities; returns grouped results.
    Roman Urdu: Saare major entities mein search karo; grouped results 
    return karo.
    """
    like = f'%{q.strip()}%'
    tenant_id = current_user.tenant_id

    # Students
    students = (
        db.query(Student)
        .filter(
            Student.tenant_id == tenant_id,
            or_(
                Student.first_name.ilike(like),
                Student.last_name.ilike(like),
                Student.email.ilike(like),
                Student.student_number.ilike(like),
            ),
        )
        .limit(LIMIT_PER_CATEGORY)
        .all()
    )

    # Courses
    courses = (
        db.query(Course)
        .filter(
            Course.tenant_id == tenant_id,
            or_(
                Course.course_code.ilike(like),
                Course.title.ilike(like),
                Course.department.ilike(like),
            ),
        )
        .limit(LIMIT_PER_CATEGORY)
        .all()
    )

    # Documents (title only — content search would be slow at scale)
    documents = (
        db.query(Document)
        .filter(
            Document.tenant_id == tenant_id,
            Document.title.ilike(like),
        )
        .limit(LIMIT_PER_CATEGORY)
        .all()
    )

    # Agents (from registry — global)
    lowered = q.lower().strip()
    agent_hits = [
        {'name': a['name'], 'description': a.get('description', '')}
        for a in registry.list_agents()
        if lowered in a['name'].lower() or lowered in (a.get('description') or '').lower()
    ][:LIMIT_PER_CATEGORY]

    # Tools (from registry — global)
    tool_hits = [
        {'name': t['name'], 'description': t.get('description', '')}
        for t in tool_registry.list()
        if lowered in t['name'].lower() or lowered in (t.get('description') or '').lower()
    ][:LIMIT_PER_CATEGORY]

    return {
        'query': q,
        'students': [
            {
                'id': s.id,
                'student_number': s.student_number,
                'name': f'{s.first_name} {s.last_name}',
                'email': s.email,
                'url': '/students',
            }
            for s in students
        ],
        'courses': [
            {
                'id': c.id,
                'course_code': c.course_code,
                'title': c.title,
                'department': c.department,
                'url': '/courses',
            }
            for c in courses
        ],
        'documents': [
            {
                'id': d.id,
                'title': d.title,
                'category': d.category,
                'url': '/knowledge',
            }
            for d in documents
        ],
        'agents': [
            {
                'name': a['name'],
                'description': a['description'],
                'url': '/agents',
            }
            for a in agent_hits
        ],
        'tools': [
            {
                'name': t['name'],
                'description': t['description'],
                'url': '/tools',
            }
            for t in tool_hits
        ],
    }
