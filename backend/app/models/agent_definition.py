"""
English: AgentDefinition — DB-backed agent metadata (description, capabilities, status).
Roman Urdu: AgentDefinition — DB mein rakhi agent metadata (description, capabilities, status).
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from backend.app.core.database import Base


class AgentDefinition(Base):
    __tablename__ = 'agent_definitions'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    capabilities_json = Column(Text, nullable=False, default='[]')
    supported_tools_json = Column(Text, nullable=False, default='[]')
    version = Column(String, nullable=False, default='1.0.0')
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    status = Column(String, nullable=False, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', name='uq_agent_tenant_name'),
    )
