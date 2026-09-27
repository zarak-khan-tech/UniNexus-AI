"""
English: Academic read-only tools. Agents use these instead of writing raw DB queries.
Roman Urdu: Academic read-only tools. Agents inhen use karte hain instead of raw DB queries.
"""
from typing import Optional
from sqlalchemy import or_

from backend.app.tools.base import BaseTool, ToolResult, PermissionLevel
from backend.app.core.database import SessionLocal
from backend.app.models.student import Student
from backend.app.models.enrollment import Enrollment
from backend.app.models.course import Course


class StudentLookupTool(BaseTool):
    name = 'student_lookup'
    description = 'Find students by student number, email, or name substring. Returns matching student records.'
    permission = PermissionLevel.READ
    input_schema = {
        'type': 'object',
        'properties': {
            'query': {'type': 'string', 'description': 'Student number, email, or name substring'},
            'limit': {'type': 'integer', 'description': 'Max results (default 20)'},
        },
        'required': ['query'],
    }

    def execute(self, query: str = '', limit: int = 20, **kwargs) -> ToolResult:
        if not query or not query.strip():
            return ToolResult(success=False, error='query parameter is required')

        db = SessionLocal()
        try:
            q = query.strip().lower()
            like = f'%{q}%'
            matches = (
                db.query(Student)
                .filter(or_(
                    Student.student_number.ilike(like),
                    Student.email.ilike(like),
                    Student.first_name.ilike(like),
                    Student.last_name.ilike(like),
                ))
                .limit(limit)
                .all()
            )
            return ToolResult(
                success=True,
                data=[
                    {
                        'student_id': s.id,
                        'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'email': s.email,
                        'enrollment_year': s.enrollment_year,
                    }
                    for s in matches
                ],
                metadata={'count': len(matches), 'query': query},
            )
        finally:
            db.close()


class ListStudentsTool(BaseTool):
    name = 'list_students'
    description = 'List all students in the institution. Optionally filter by enrollment year.'
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
                        'student_id': s.id,
                        'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'email': s.email,
                        'enrollment_year': s.enrollment_year,
                    }
                    for s in students
                ],
                metadata={'count': len(students)},
            )
        finally:
            db.close()


class AttendanceQueryTool(BaseTool):
    name = 'attendance_query'
    description = 'Find students with attendance below a threshold. Returns enrollment-level rows including course and grade.'
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
                        'student_id': s.id,
                        'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'course_code': c.course_code,
                        'course_title': c.title,
                        'attendance_percentage': e.attendance_percentage,
                        'grade': e.grade,
                    }
                    for e, s, c in rows
                ],
                metadata={'count': len(rows), 'threshold': threshold},
            )
        finally:
            db.close()


class ListEnrollmentsTool(BaseTool):
    name = 'list_enrollments'
    description = 'List all enrollments (student + course + attendance + grade). Used for risk analysis.'
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
                        'student_id': s.id,
                        'student_number': s.student_number,
                        'name': f'{s.first_name} {s.last_name}',
                        'attendance_percentage': e.attendance_percentage,
                        'grade': e.grade,
                    }
                    for e, s in rows
                ],
                metadata={'count': len(rows)},
            )
        finally:
            db.close()
