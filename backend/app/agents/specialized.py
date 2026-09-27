from backend.app.agents.base import BaseAgent
from backend.app.core.database import SessionLocal
from backend.app.tools import tool_registry
from backend.app.models.enrollment import Enrollment
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.document import Document
from typing import Dict, Any


# =============================================================================
# AttendanceAgent — uses attendance_query tool
# =============================================================================
class AttendanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name='AttendanceAgent',
            description='Finds students with low attendance via the attendance_query tool.'
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # English: Default threshold; if the request mentions a number like "80%", use it.
        # Roman Urdu: Default threshold; agar request mein 80% jaisa number ho to wahi use karo.
        import re
        threshold = 75.0
        request = task.get('request', '').lower()
        match = re.search(r'(\d{2,3})\s*%', request)
        if match:
            try:
                threshold = float(match.group(1))
            except ValueError:
                pass

        result = tool_registry.call('attendance_query', threshold=threshold)

        if not result.success:
            return {
                'status': 'error',
                'agent': self.name,
                'tool_used': 'attendance_query',
                'error': result.error,
            }

        # English: Shape output for frontend — same as before (course_code → course).
        # Roman Urdu: Frontend ke liye output shape banao — pehle jaisa hi (course_code → course).
        rows = result.data or []
        return {
            'status': 'success',
            'agent': self.name,
            'tool_used': 'attendance_query',
            'total_flagged': len(rows),
            'threshold': threshold,
            'data': [
                {
                    'student_id': r['student_id'],
                    'student_number': r['student_number'],
                    'name': r['name'],
                    'course': r['course_code'],
                    'attendance_percentage': r['attendance_percentage'],
                }
                for r in rows
            ],
        }


# =============================================================================
# PolicyAgent — static thresholds for now (will read from documents later)
# =============================================================================
class PolicyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='PolicyAgent', description='Checks institutional policies and thresholds.')

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'success',
            'agent': self.name,
            'policy_threshold': 75,
            'rule': 'Students below 75% attendance require intervention.',
        }


# =============================================================================
# RiskAgent — uses list_enrollments tool
# =============================================================================
class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name='RiskAgent',
            description='Analyzes academic risk via the list_enrollments tool.'
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        result = tool_registry.call('list_enrollments', limit=500)

        if not result.success:
            return {
                'status': 'error',
                'agent': self.name,
                'tool_used': 'list_enrollments',
                'error': result.error,
            }

        # English: Same deterministic risk logic, but now fed by the tool.
        # Roman Urdu: Wahi deterministic risk logic, bas ab tool se data aata hai.
        risk_assessments = []
        for row in result.data or []:
            attendance = row.get('attendance_percentage', 100) or 0
            grade = row.get('grade') or ''

            if attendance < 60 or grade in ('D', 'F'):
                level = 'High'
            elif attendance < 75 or grade == 'C':
                level = 'Medium'
            else:
                level = 'Low'

            if level in ('High', 'Medium'):
                risk_assessments.append({
                    'student_id': row['student_id'],
                    'name': row['name'],
                    'attendance': attendance,
                    'grade': grade,
                    'risk_level': level,
                })

        return {
            'status': 'success',
            'agent': self.name,
            'tool_used': 'list_enrollments',
            'at_risk_students': risk_assessments,
        }


# =============================================================================
# KnowledgeAgent — unchanged for now (uses direct DB, will move to RAG later)
# =============================================================================
class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name='KnowledgeAgent',
            description='Retrieves university policies and documents using keyword search.'
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            query = task.get('request', '')
            words = [w for w in query.split() if len(w) > 3]

            q = db.query(Document)
            if words:
                from sqlalchemy import or_
                filters = [Document.content.ilike(f'%{w}%') | Document.title.ilike(f'%{w}%') for w in words]
                q = q.filter(or_(*filters))

            docs = q.limit(3).all()

            results = []
            for doc in docs:
                results.append({
                    'title': doc.title,
                    'category': doc.category,
                    'content_preview': doc.content[:200] + '...' if len(doc.content) > 200 else doc.content,
                })

            return {
                'status': 'success',
                'agent': self.name,
                'tool_used': 'direct_db_query',  # to be replaced with RAG tool later
                'total_matches': len(results),
                'documents': results,
            }
        finally:
            db.close()
