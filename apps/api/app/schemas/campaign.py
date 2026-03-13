# apps/api/app/schemas/campaign.py
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.enums import CampaignStatus, SendingMode

class CampaignBase(BaseModel):
    campaign_name: str
    target_industries: Optional[List[str]] = None
    target_locations: Optional[List[str]] = None
    target_company_size: Optional[str] = None
    target_job_titles: Optional[List[str]] = None
    offer_summary: Optional[str] = None
    value_proposition: Optional[str] = None
    sending_mode: SendingMode = SendingMode.manual_approval
    max_leads: int = 100

class CampaignCreate(CampaignBase):
    # Enforce at least one target criteria logically or using Pydantic strictly
    target_industries: List[str] = Field(default_factory=list, description="Must have at least one industry to target")

class CampaignUpdate(BaseModel):
    campaign_name: Optional[str] = None
    status: Optional[CampaignStatus] = None
    sending_mode: Optional[SendingMode] = None

class CampaignResponse(CampaignBase):
    id: UUID
    user_id: UUID
    status: CampaignStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
