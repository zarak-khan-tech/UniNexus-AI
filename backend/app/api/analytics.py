from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import Counter
from datetime import datetime, timedelta

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.models.enrollment import Enrollment
from backend.app.models.agent_execution import AgentExecution
import json

router = APIRouter(prefix='/analytics', tags=['Analytics'])

@router.get('/overview')
def analytics_overview(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    tenant_id = current_user.tenant_id

    # Risk distribution (simplified deterministic rules — same as RiskAgent)
    enrollments = db.query(Enrollment, Student).join(
        Student, Enrollment.student_id == Student.id
    ).filter(Student.tenant_id == tenant_id).all()

    risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}
    for enrollment, _ in enrollments:
        if enrollment.attendance_percentage < 60 or enrollment.grade in ['D', 'F']:
            risk_counts['High'] += 1
        elif enrollment.attendance_percentage < 75 or enrollment.grade == 'C':
            risk_counts['Medium'] += 1
        else:
            risk_counts['Low'] += 1

    # Attendance per student
    students = db.query(Student).filter(Student.tenant_id == tenant_id).all()
    attendance_data = []
    for s in students:
        s_enrollments = db.query(Enrollment).filter(Enrollment.student_id == s.id).all()
        if s_enrollments:
            avg = sum(e.attendance_percentage for e in s_enrollments) / len(s_enrollments)
            attendance_data.append({
                'name': f'{s.first_name} {s.last_name}',
                'attendance': round(avg, 1)
            })

    # Agent usage from executions
    executions = db.query(AgentExecution).filter(AgentExecution.tenant_id == tenant_id).all()
    agent_counter = Counter()
    for ex in executions:
        try:
            plan = json.loads(ex.execution_plan_json)
            for step in plan:
                agent_counter[step.get('agent', 'Unknown')] += 1
        except Exception:
            pass
    agent_usage = [{'agent': k, 'count': v} for k, v in agent_counter.most_common()]

    # Executions over last 7 days
    today = datetime.utcnow().date()
    daily = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = sum(1 for ex in executions if ex.created_at.date() == day)
        daily.append({'date': day.strftime('%b %d'), 'executions': count})

    return {
        'risk_distribution': risk_counts,
        'attendance_by_student': attendance_data,
        'agent_usage': agent_usage,
        'executions_by_day': daily,
        'total_executions': len(executions),
    }
