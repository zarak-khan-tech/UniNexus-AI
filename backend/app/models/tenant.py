"""
English: Tenant model — represents one university. Settings live in a JSON blob.
Roman Urdu: Tenant model — ek university. Settings JSON blob mein.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base


class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    domain = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    settings_json = Column(Text, nullable=False, default='{}')

    users = relationship('User', back_populates='tenant')
