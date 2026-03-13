import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Text, Boolean
from app.models.base import Base, generate_uuid
from app.models.enums import OutreachStatus

class OutreachMessage(Base):
    __tablename__ = "outreach_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid, index=True)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    status = Column(SQLEnum(OutreachStatus), default=OutreachStatus.drafting, nullable=False)
    
    approved_by_user = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
