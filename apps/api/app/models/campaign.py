import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Integer, Text
from app.models.base import Base, generate_uuid
from app.models.enums import CampaignStatus, SendingMode

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    campaign_name = Column(String, nullable=False)
    target_industries = Column(ARRAY(String), nullable=True)
    target_locations = Column(ARRAY(String), nullable=True)
    target_company_size = Column(String, nullable=True)
    target_job_titles = Column(ARRAY(String), nullable=True)
    offer_summary = Column(Text, nullable=True)
    value_proposition = Column(Text, nullable=True)
    
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.draft, nullable=False)
    sending_mode = Column(SQLEnum(SendingMode), default=SendingMode.manual_approval, nullable=False)
    max_leads = Column(Integer, default=100)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
