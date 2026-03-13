# apps/api/app/schemas/lead.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.models.enums import LeadStatus

class LeadBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    company_name: Optional[str] = None

class LeadCreate(LeadBase):
    campaign_id: UUID
    scraped_data_json: Optional[Dict[str, Any]] = None

class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    qualification_score: Optional[float] = None
    qualification_reason: Optional[str] = None

class LeadResponse(LeadBase):
    id: UUID
    campaign_id: UUID
    status: LeadStatus
    qualification_score: Optional[float] = None
    qualification_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
