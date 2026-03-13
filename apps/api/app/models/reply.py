from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, generate_uuid
import enum

class ReplyClassification(str, enum.Enum):
    interested = "interested"
    not_interested = "not_interested"
    ask_later = "ask_later"
    bounced = "bounced"
    out_of_office = "out_of_office"
    neutral = "neutral"

class Reply(Base):
    __tablename__ = "replies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    outreach_message_id = Column(UUID(as_uuid=True), nullable=False) # FK
    lead_id = Column(UUID(as_uuid=True), nullable=False) # FK
    
    provider_thread_id = Column(String, nullable=True)
    reply_text = Column(String, nullable=True)
    
    classification = Column(Enum(ReplyClassification), nullable=True)
    sentiment = Column(String, nullable=True)
    extracted_intent = Column(String, nullable=True)
    
    received_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
