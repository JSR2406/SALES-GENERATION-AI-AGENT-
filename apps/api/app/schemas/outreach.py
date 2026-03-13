# apps/api/app/schemas/outreach.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.enums import OutreachStatus

class OutreachBase(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None

class OutreachCreate(OutreachBase):
    campaign_id: UUID
    lead_id: UUID
    status: OutreachStatus = OutreachStatus.drafting

class OutreachUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    status: Optional[OutreachStatus] = None
    approved_by_user: Optional[bool] = None

class OutreachResponse(OutreachBase):
    id: UUID
    campaign_id: UUID
    lead_id: UUID
    status: OutreachStatus
    approved_by_user: bool
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
