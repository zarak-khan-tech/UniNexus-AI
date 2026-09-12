from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from backend.app.core.database import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True) # e.g., 'Policy', 'Handbook'
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
