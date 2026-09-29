"""
English: Notification model — user-facing alerts for events like approvals, executions.
Roman Urdu: Notification model — user ke liye alerts (approvals, executions).
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from datetime import datetime
from backend.app.core.database import Base


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    kind = Column(String, nullable=False, default='system', index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    action_url = Column(String, nullable=True)

    is_read = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
