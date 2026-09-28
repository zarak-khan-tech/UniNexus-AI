"""
English: Academic read-only tools with explicit trigger descriptions.
Roman Urdu: Academic read-only tools, explicit trigger descriptions ke saath.
"""
from typing import Optional
from sqlalchemy import or_, and_
from backend.app.tools.base import BaseTool, ToolResult, PermissionLevel
from backend.app.core.database import SessionLocal
from backend.app.models.student import Student
from backend.app.models.enrollment import Enrollment
from backend.app.models.course import Course


class StudentLookupTool(BaseTool):
    name = 'student_lookup'
    description = (
        'Find students by student number, email, or FULL NAME (first and last). '
        'USE THIS whenever the user asks "find student X", "who is S101", '
        '"tell me about student <name>", or any request to look up an '
        'individual student record.'
    )
    permission = PermissionLevel.READ
    input_schema = {
        'type': 'object',
        'properties': {
            'query': {'type': 'string', 'description': 'Student number, email, or full name like "Ali Khan"'},
            'limit': {'type': 'integer', 'description': 'Max results (default 20)'},
        },
        'required': ['query'],
    }

    def execute(self, query: str = '', limit: int = 20, **kwargs) -> ToolResult:
        if not query or not query.strip():
            return ToolResult(success=False, error='query parameter is required')
        db = SessionLocal()
        try:
            q = query.strip()
            like = f'%{q}%'
            tokens = [t for t in q.split() if t]

            # English: Try full-string match first (works for numbers/emails).
            # Roman Urdu: Pehle full-string match (numbers/emails ke liye).
            base_filter = or_(
                Student.student_number.ilike(like),
                Student.email.ilike(like),
                Student.first_name.ilike(like),
                Student.last_name.ilike(like),
            )

            # English: If query has multiple words, also try token-wise match
            # across first_name AND last_name.
            # Roman Urdu: Agar query mein multiple words hain to first_name aur
            # last_name pe token-wise match bhi try karo.
            if len(tokens) >= 2:
                token_filters = [
                    or_(
                        Student.first_name.ilike(f'%{t}%'),
                        Student.last_name.ilike(f'%{t}%'),
                        Student.student_number.ilike(f'%{t}%'),
                        Student.email.ilike(f'%{t}%'),
                    )
                    for t in tokens
                ]
                full_filter = and_(*token_filters)
                matches = (
                    db.query(Student)
                    .filter(or_(base_filter, full_filter))
                    .limit(limit)
                    .all()
                )
            else:
                matches = db.query(Student).filter(base_filter).limit(limit).all()

            return ToolResult(
                success=True,
                data=[
                    {
                        'student_id': s.id, 'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'email': s.email, 'enrollment_year': s.enrollment_year,
                    } for s in matches
                ],
                metadata={'count': len(matches), 'query': query},
            )
        finally:
            db.close()


class ListStudentsTool(BaseTool):
    name = 'list_students'
    description = (
        'List all students in the institution. Optionally filter by enrollment year. '
        'USE THIS for "list all students", "show me everyone", "how many students".'
    )
    permission = PermissionLevel.READ
    input_schema = {
        'type': 'object',
        'properties': {
            'enrollment_year': {'type': 'integer', 'description': 'Optional enrollment year filter'},
            'limit': {'type': 'integer', 'description': 'Max results (default 50)'},
        },
    }

    def execute(self, enrollment_year: Optional[int] = None, limit: int = 50, **kwargs) -> ToolResult:
        db = SessionLocal()
        try:
            q = db.query(Student)
            if enrollment_year:
                q = q.filter(Student.enrollment_year == enrollment_year)
            students = q.limit(limit).all()
            return ToolResult(
                success=True,
                data=[
                    {
                        'student_id': s.id, 'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'email': s.email, 'enrollment_year': s.enrollment_year,
                    } for s in students
                ],
                metadata={'count': len(students)},
            )
        finally:
            db.close()


class AttendanceQueryTool(BaseTool):
    name = 'attendance_query'
    description = (
        'Finds students with attendance BELOW a threshold by querying the database. '
        'ALWAYS USE THIS whenever the user asks: '
        '"show me students with low attendance", "which students have poor attendance", '
        '"list students below 75%", "who is not attending class", '
        '"find students with attendance issues". '
        'Returns real students with their attendance percentages per course.'
    )
    permission = PermissionLevel.READ
    input_schema = {
        'type': 'object',
        'properties': {
            'threshold': {'type': 'number', 'description': 'Attendance percentage threshold (default 75)'},
            'limit': {'type': 'integer', 'description': 'Max results (default 100)'},
        },
    }

    def execute(self, threshold: float = 75.0, limit: int = 100, **kwargs) -> ToolResult:
        db = SessionLocal()
        try:
            rows = (
                db.query(Enrollment, Student, Course)
                .join(Student, Enrollment.student_id == Student.id)
                .join(Course, Enrollment.course_id == Course.id)
                .filter(Enrollment.attendance_percentage < threshold)
                .limit(limit)
                .all()
            )
            return ToolResult(
                success=True,
                data=[
                    {
                        'student_id': s.id, 'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'course_code': c.course_code, 'course_title': c.title,
                        'attendance_percentage': e.attendance_percentage, 'grade': e.grade,
                    } for e, s, c in rows
                ],
                metadata={'count': len(rows), 'threshold': threshold},
            )
        finally:
            db.close()


class ListEnrollmentsTool(BaseTool):
    name = 'list_enrollments'
    description = (
        'List all enrollments (student + course + attendance + grade). '
        'USE THIS for risk analysis, "which students might fail", '
        '"who has bad grades", "show at-risk students".'
    )
    permission = PermissionLevel.READ
    input_schema = {
        'type': 'object',
        'properties': {
            'limit': {'type': 'integer', 'description': 'Max results (default 500)'},
        },
    }

    def execute(self, limit: int = 500, **kwargs) -> ToolResult:
        db = SessionLocal()
        try:
            rows = (
                db.query(Enrollment, Student)
                .join(Student, Enrollment.student_id == Student.id)
                .limit(limit)
                .all()
            )
            return ToolResult(
                success=True,
                data=[
                    {
                        'student_id': s.id, 'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'attendance_percentage': e.attendance_percentage, 'grade': e.grade,
                    } for e, s in rows
                ],
                metadata={'count': len(rows)},
            )
        finally:
            db.close()
