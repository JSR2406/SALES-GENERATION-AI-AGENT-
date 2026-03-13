# apps/api/app/services/campaign_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from uuid import UUID
from typing import List, Optional

from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.models.enums import CampaignStatus

class CampaignService:
    @staticmethod
    async def create_campaign(db: AsyncSession, obj_in: CampaignCreate, user_id: UUID) -> Campaign:
        db_obj = Campaign(**obj_in.model_dump(), user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def get_my_campaigns(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Campaign]:
        result = await db.execute(
            select(Campaign).where(Campaign.user_id == user_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_my_campaign(db: AsyncSession, campaign_id: UUID, user_id: UUID) -> Optional[Campaign]:
        result = await db.execute(
            select(Campaign).where(Campaign.id == campaign_id, Campaign.user_id == user_id)
        )
        return result.scalars().first()

    @staticmethod
    async def update_campaign(db: AsyncSession, campaign_id: UUID, user_id: UUID, obj_in: CampaignUpdate) -> Optional[Campaign]:
        campaign = await CampaignService.get_my_campaign(db, campaign_id, user_id)
        if not campaign:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)
            
        await db.commit()
        await db.refresh(campaign)
        return campaign
        
    @staticmethod
    async def update_campaign_status(db: AsyncSession, campaign_id: UUID, user_id: UUID, status: CampaignStatus) -> Optional[Campaign]:
        return await CampaignService.update_campaign(db, campaign_id, user_id, CampaignUpdate(status=status))
