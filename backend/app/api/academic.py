"""
English: Add a semantic search endpoint for the Knowledge Base UI.
Roman Urdu: Knowledge Base UI ke liye semantic search endpoint.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.enrollment import Enrollment
from backend.app.models.document import Document
from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store

router = APIRouter(prefix='/academic', tags=['Academic Directory'])

@router.get('/students')
def list_students(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.tenant_id == current_user.tenant_id).all()
    results = []
    for s in students:
        enrollments = db.query(Enrollment).filter(Enrollment.student_id == s.id).all()
        total_courses = len(enrollments)
        avg_attendance = (sum(e.attendance_percentage for e in enrollments) / total_courses) if total_courses > 0 else 0
        results.append({
            'id': s.id, 'student_number': s.student_number,
            'first_name': s.first_name, 'last_name': s.last_name,
            'email': s.email, 'enrollment_year': s.enrollment_year,
            'total_courses': total_courses, 'average_attendance': round(avg_attendance, 1),
        })
    return {'total': len(results), 'students': results}

@router.get('/courses')
def list_courses(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.tenant_id == current_user.tenant_id).all()
    results = []
    for c in courses:
        count = db.query(Enrollment).filter(Enrollment.course_id == c.id).count()
        results.append({
            'id': c.id, 'course_code': c.course_code, 'title': c.title,
            'credit_hours': c.credit_hours, 'department': c.department,
            'enrolled_students': count,
        })
    return {'total': len(results), 'courses': results}

@router.get('/documents')
def list_documents(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.tenant_id == current_user.tenant_id).all()
    return {
        'total': len(docs),
        'documents': [
            {'id': d.id, 'title': d.title, 'category': d.category,
             'content': d.content, 'created_at': d.created_at.isoformat()}
            for d in docs
        ],
    }

@router.get('/documents/search')
def search_documents(
    q: str = Query(..., min_length=2),
    top_k: int = 5,
    current_user: User = Depends(get_current_active_user),
):
    """
    English: Semantic search over documents using vector embeddings.
    Roman Urdu: Vector embeddings ke zariye documents pe semantic search.
    """
    if not q.strip():
        return {'total': 0, 'query': q, 'documents': []}

    vec = embedding_service.embed(q)
    if not vec:
        return {'total': 0, 'query': q, 'documents': [], 'error': 'embedding failed'}

    results = vector_store.search(vec, top_k=top_k)

    # English: Filter by tenant.
    # Roman Urdu: Tenant se filter karo.
    results = [r for r in results if r.get('tenant_id') == current_user.tenant_id]

    docs = []
    for r in results:
        content = r.get('content', '') or ''
        docs.append({
            'id': r.get('id'),
            'title': r.get('title'),
            'category': r.get('category'),
            'content': content,
            'content_preview': (content[:280] + '…') if len(content) > 280 else content,
            'similarity': r.get('similarity'),
        })

    return {'total': len(docs), 'query': q, 'documents': docs}
