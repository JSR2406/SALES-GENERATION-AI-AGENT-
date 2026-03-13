import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Boolean
from app.models.base import Base, generate_uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
