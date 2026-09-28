"""
English: Write tools. Write-lower actions auto-execute; write-higher actions
         require human approval before they run.
Roman Urdu: Write tools. Low-risk writes auto-chalte hain; high-risk writes
            ko pehle insaan ki approval chahiye.
"""
from backend.app.tools.base import BaseTool, ToolResult, PermissionLevel
from backend.app.core.database import SessionLocal
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.enrollment import Enrollment
from datetime import datetime


class UpdateStudentGradeTool(BaseTool):
    name = 'update_student_grade'
    description = (
        'HIGH-RISK: Update a student grade in the database. '
        'Requires human approval before execution. '
        'Args: student_number (e.g. S101), course_code (e.g. MATH101), new_grade (e.g. A, B+, C).'
    )
    permission = PermissionLevel.WRITE_HIGH
    input_schema = {
        'type': 'object',
        'properties': {
            'student_number': {'type': 'string', 'description': 'Student number, e.g. S101'},
            'course_code': {'type': 'string', 'description': 'Course code, e.g. MATH101'},
            'new_grade': {'type': 'string', 'description': 'New letter grade (A, B+, C, D, F)'},
        },
        'required': ['student_number', 'course_code', 'new_grade'],
    }

    def execute(self, student_number: str = '', course_code: str = '',
                new_grade: str = '', **kwargs) -> ToolResult:
        if not student_number or not course_code or not new_grade:
            return ToolResult(success=False, error='Missing required args')
        db = SessionLocal()
        try:
            student = db.query(Student).filter(Student.student_number == student_number).first()
            if not student:
                return ToolResult(success=False, error=f'Student {student_number} not found')
            course = db.query(Course).filter(Course.course_code == course_code).first()
            if not course:
                return ToolResult(success=False, error=f'Course {course_code} not found')
            enrollment = db.query(Enrollment).filter(
                Enrollment.student_id == student.id,
                Enrollment.course_id == course.id,
            ).first()
            if not enrollment:
                return ToolResult(success=False, error=f'No enrollment for {student_number} in {course_code}')

            old_grade = enrollment.grade
            enrollment.grade = new_grade.upper().strip()
            db.commit()
            return ToolResult(
                success=True,
                data={
                    'student_number': student_number,
                    'student_name': f'{student.first_name} {student.last_name}',
                    'course_code': course_code,
                    'old_grade': old_grade,
                    'new_grade': enrollment.grade,
                    'updated_at': datetime.utcnow().isoformat(),
                },
                metadata={'action': 'grade_updated'},
            )
        finally:
            db.close()


class SendStudentNotificationTool(BaseTool):
    name = 'send_student_notification'
    description = (
        'LOW-RISK: Send a notification to a student (stored in the DB as a message record). '
        'Auto-executes; no approval needed. '
        'Args: student_number (e.g. S101), message (short text).'
    )
    permission = PermissionLevel.WRITE_LOW
    input_schema = {
        'type': 'object',
        'properties': {
            'student_number': {'type': 'string', 'description': 'Student number, e.g. S101'},
            'message': {'type': 'string', 'description': 'Notification message text'},
        },
        'required': ['student_number', 'message'],
    }

    def execute(self, student_number: str = '', message: str = '', **kwargs) -> ToolResult:
        if not student_number or not message:
            return ToolResult(success=False, error='Missing required args')
        db = SessionLocal()
        try:
            student = db.query(Student).filter(Student.student_number == student_number).first()
            if not student:
                return ToolResult(success=False, error=f'Student {student_number} not found')
            # English: Stub — in production this would send an email/SMS.
            # Roman Urdu: Stub — production mein email/SMS bhejta hai.
            return ToolResult(
                success=True,
                data={
                    'student_number': student_number,
                    'student_name': f'{student.first_name} {student.last_name}',
                    'message': message,
                    'delivered_at': datetime.utcnow().isoformat(),
                },
                metadata={'action': 'notification_sent'},
            )
        finally:
            db.close()
