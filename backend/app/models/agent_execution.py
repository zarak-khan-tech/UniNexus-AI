from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from datetime import datetime
from backend.app.core.database import Base

class AgentExecution(Base):
    __tablename__ = 'agent_executions'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_email = Column(String, nullable=False)
    original_request = Column(Text, nullable=False)
    status = Column(String, nullable=False, default='completed')
    execution_plan_json = Column(Text, nullable=False)
    execution_results_json = Column(Text, nullable=False)
    duration_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
