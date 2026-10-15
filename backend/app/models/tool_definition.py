"""
English: ToolDefinition — DB-backed tool metadata (description, permission, 
schema, active state). Actual execution logic still lives in tool classes.
Roman Urdu: ToolDefinition — DB mein rakhi tool metadata. Actual execution 
logic abhi bhi tool classes mein hai.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from backend.app.core.database import Base


class ToolDefinition(Base):
    __tablename__ = 'tool_definitions'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    permission = Column(String, nullable=False, default='read')
    input_schema_json = Column(Text, nullable=False, default='{}')
    version = Column(String, nullable=False, default='1.0.0')
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', name='uq_tool_tenant_name'),
    )
