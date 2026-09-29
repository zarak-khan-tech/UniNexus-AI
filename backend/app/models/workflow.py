"""
English: Workflow model — event-driven automation rules.
Roman Urdu: Workflow model — event-driven automation rules.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from datetime import datetime
from backend.app.core.database import Base


class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # English: Trigger types: 'attendance_below', 'execution_completed'.
    # Roman Urdu: Trigger types: 'attendance_below', 'execution_completed'.
    trigger_type = Column(String, nullable=False, index=True)
    trigger_config_json = Column(Text, nullable=False, default='{}')

    # English: Action types: 'send_notification', 'log_only'.
    # Roman Urdu: Action types: 'send_notification', 'log_only'.
    action_type = Column(String, nullable=False)
    action_config_json = Column(Text, nullable=False, default='{}')

    is_active = Column(Boolean, nullable=False, default=True, index=True)
    last_run_at = Column(DateTime, nullable=True)
    run_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
