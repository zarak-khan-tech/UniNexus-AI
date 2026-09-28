"""
English: Approval model — tracks high-risk agent actions pending human review.
Roman Urdu: Approval model — high-risk agent actions jo human review ka intezaar kar rahe hain.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from backend.app.core.database import Base


class Approval(Base):
    __tablename__ = 'approvals'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_email = Column(String, nullable=False)

    # English: The high-risk action that was requested.
    # Roman Urdu: Wo high-risk action jo request hua.
    tool_name = Column(String, nullable=False)
    args_json = Column(Text, nullable=False)
    action_description = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=True)

    # English: Workflow status.
    # Roman Urdu: Workflow ka status.
    status = Column(String, nullable=False, default='pending', index=True)

    # English: Populated when the action is finally executed (on approve).
    # Roman Urdu: Jab action execute ho jaye (approve pe) tab populate hota hai.
    result_json = Column(Text, nullable=True)
    error = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by_email = Column(String, nullable=True)
