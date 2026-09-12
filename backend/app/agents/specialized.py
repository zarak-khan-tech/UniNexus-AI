from backend.app.agents.base import BaseAgent
from backend.app.core.database import SessionLocal
from backend.app.models.enrollment import Enrollment
from backend.app.models.student import Student
from backend.app.models.course import Course
from typing import Dict, Any

class AttendanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='AttendanceAgent', description='Analyzes student attendance data from the database.')
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            # Get all enrollments with attendance below 75%
            low_attendance = db.query(Enrollment, Student, Course).join(
                Student, Enrollment.student_id == Student.id
            ).join(
                Course, Enrollment.course_id == Course.id
            ).filter(Enrollment.attendance_percentage < 75).all()
            
            results = []
            for enrollment, student, course in low_attendance:
                results.append({
                    'student_id': student.id,
                    'student_number': student.student_number,
                    'name': f'{student.first_name} {student.last_name}',
                    'course': course.course_code,
                    'attendance_percentage': enrollment.attendance_percentage
                })
            
            return {
                'status': 'success',
                'agent': self.name,
                'total_flagged': len(results),
                'data': results
            }
        finally:
            db.close()

class PolicyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='PolicyAgent', description='Checks institutional policies and thresholds.')
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Policy threshold (would eventually be read from a policy document table)
        return {
            'status': 'success',
            'agent': self.name,
            'policy_threshold': 75,
            'rule': 'Students below 75% attendance require intervention.'
        }

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='RiskAgent', description='Analyzes academic risk based on data and policy.')
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            # Combine low attendance + low grades into a risk score
            at_risk = db.query(Enrollment, Student).join(
                Student, Enrollment.student_id == Student.id
            ).all()
            
            risk_assessments = []
            for enrollment, student in at_risk:
                # Simple deterministic risk logic (AI reasoning comes later)
                if enrollment.attendance_percentage < 60 or enrollment.grade in ['D', 'F']:
                    level = 'High'
                elif enrollment.attendance_percentage < 75 or enrollment.grade == 'C':
                    level = 'Medium'
                else:
                    level = 'Low'
                
                if level in ['High', 'Medium']:
                    risk_assessments.append({
                        'student_id': student.id,
                        'name': f'{student.first_name} {student.last_name}',
                        'attendance': enrollment.attendance_percentage,
                        'grade': enrollment.grade,
                        'risk_level': level
                    })
            
            return {
                'status': 'success',
                'agent': self.name,
                'at_risk_students': risk_assessments
            }
        finally:
            db.close()

from backend.app.models.document import Document
from sqlalchemy import or_

class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='KnowledgeAgent', description='Retrieves university policies and documents using keyword search.')

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            query = task.get('request', '')
            words = [w for w in query.split() if len(w) > 3]
            
            q = db.query(Document)
            if words:
                filters = [Document.content.ilike(f'%{w}%') | Document.title.ilike(f'%{w}%') for w in words]
                q = q.filter(or_(*filters))
            
            docs = q.limit(3).all()
            
            results = []
            for doc in docs:
                results.append({
                    'title': doc.title,
                    'category': doc.category,
                    'content_preview': doc.content[:200] + '...' if len(doc.content) > 200 else doc.content
                })
            
            return {
                'status': 'success',
                'agent': self.name,
                'total_matches': len(results),
                'documents': results
            }
        finally:
            db.close()
