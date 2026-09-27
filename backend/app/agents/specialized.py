from backend.app.agents.base import BaseAgent
from backend.app.core.database import SessionLocal
from backend.app.tools import tool_registry
from backend.app.models.enrollment import Enrollment
from backend.app.models.student import Student
from backend.app.models.course import Course
from backend.app.models.document import Document
from typing import Dict, Any


class AttendanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='AttendanceAgent', description='Finds students with low attendance via the attendance_query tool.')

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
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
            return {'status': 'error', 'agent': self.name, 'tool_used': 'attendance_query', 'error': result.error}
        rows = result.data or []
        return {
            'status': 'success', 'agent': self.name, 'tool_used': 'attendance_query',
            'total_flagged': len(rows), 'threshold': threshold,
            'data': [
                {
                    'student_id': r['student_id'], 'student_number': r['student_number'],
                    'name': r['name'], 'course': r['course_code'],
                    'attendance_percentage': r['attendance_percentage'],
                } for r in rows
            ],
        }


class PolicyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='PolicyAgent', description='Checks institutional policies and thresholds.')

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'success', 'agent': self.name,
            'policy_threshold': 75,
            'rule': 'Students below 75% attendance require intervention.',
        }


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='RiskAgent', description='Analyzes academic risk via the list_enrollments tool.')

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        result = tool_registry.call('list_enrollments', limit=500)
        if not result.success:
            return {'status': 'error', 'agent': self.name, 'tool_used': 'list_enrollments', 'error': result.error}
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
                    'student_id': row['student_id'], 'name': row['name'],
                    'attendance': attendance, 'grade': grade, 'risk_level': level,
                })
        return {'status': 'success', 'agent': self.name, 'tool_used': 'list_enrollments', 'at_risk_students': risk_assessments}


class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='KnowledgeAgent', description='Retrieves university documents via semantic vector search (RAG).')

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        query = (task.get('request') or '').strip()
        result = tool_registry.call('semantic_search', query=query, top_k=3)
        if not result.success:
            return {'status': 'error', 'agent': self.name, 'tool_used': 'semantic_search', 'error': result.error}

        docs = result.data or []
        # English: Tool returns 'content'; build preview here for the frontend UI.
        # Roman Urdu: Tool 'content' return karta hai; preview yahan banate hain frontend UI ke liye.
        documents = []
        for d in docs:
            content = d.get('content', '') or ''
            preview = (content[:320] + '...') if len(content) > 320 else content
            documents.append({
                'title': d.get('title'),
                'category': d.get('category'),
                'content_preview': preview,
                'similarity': d.get('similarity'),
            })

        return {
            'status': 'success', 'agent': self.name, 'tool_used': 'semantic_search',
            'total_matches': len(documents),
            'documents': documents,
        }
