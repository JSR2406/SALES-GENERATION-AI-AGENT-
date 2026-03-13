import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Float, Text
from app.models.base import Base, generate_uuid
from app.models.enums import LeadStatus

class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid, index=True)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    scraped_data_json = Column(JSONB, nullable=True)
    
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.discovered, nullable=False)
    qualification_score = Column(Float, nullable=True)
    qualification_reason = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
