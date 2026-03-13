# apps/api/app/services/lead_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from uuid import UUID
from typing import List, Optional

from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate
from app.models.enums import LeadStatus

class LeadService:
    @staticmethod
    async def create_lead(db: AsyncSession, obj_in: LeadCreate) -> Lead:
        db_obj = Lead(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def get_campaign_leads(db: AsyncSession, campaign_id: UUID, skip: int = 0, limit: int = 100) -> List[Lead]:
        result = await db.execute(
            select(Lead).where(Lead.campaign_id == campaign_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_lead(db: AsyncSession, lead_id: UUID) -> Optional[Lead]:
        result = await db.execute(select(Lead).where(Lead.id == lead_id))
        return result.scalars().first()

    @staticmethod
    async def update_lead(db: AsyncSession, lead_id: UUID, obj_in: LeadUpdate) -> Optional[Lead]:
        lead = await LeadService.get_lead(db, lead_id)
        if not lead:
            return None
            
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lead, field, value)
            
        await db.commit()
        await db.refresh(lead)
        return lead
        
    @staticmethod
    async def bulk_update_lead_status(db: AsyncSession, lead_ids: List[UUID], status: LeadStatus) -> None:
        await db.execute(
            update(Lead)
            .where(Lead.id.in_(lead_ids))
            .values(status=status)
        )
        await db.commit()
