from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.enrollment import Enrollment

router = APIRouter(prefix='/academic', tags=['Academic Directory'])

@router.get('/students')
def list_students(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    '''Returns all students for the current tenant with aggregate enrollment stats.'''
    students = db.query(Student).filter(Student.tenant_id == current_user.tenant_id).all()
    
    results = []
    for s in students:
        enrollments = db.query(Enrollment).filter(Enrollment.student_id == s.id).all()
        total_courses = len(enrollments)
        avg_attendance = (
            sum(e.attendance_percentage for e in enrollments) / total_courses
            if total_courses > 0 else 0
        )
        results.append({
            'id': s.id,
            'student_number': s.student_number,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'email': s.email,
            'enrollment_year': s.enrollment_year,
            'total_courses': total_courses,
            'average_attendance': round(avg_attendance, 1),
        })
    return {'total': len(results), 'students': results}

@router.get('/courses')
def list_courses(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    '''Returns all courses for the current tenant with enrollment counts.'''
    courses = db.query(Course).filter(Course.tenant_id == current_user.tenant_id).all()
    
    results = []
    for c in courses:
        enrollment_count = db.query(Enrollment).filter(Enrollment.course_id == c.id).count()
        results.append({
            'id': c.id,
            'course_code': c.course_code,
            'title': c.title,
            'credit_hours': c.credit_hours,
            'department': c.department,
            'enrolled_students': enrollment_count,
        })
    return {'total': len(results), 'courses': results}
