# apps/api/app/api/routes/leads.py
from fastapi import APIRouter, HTTPException
from app.core.supabase import supabase
from uuid import UUID

router = APIRouter()

@router.get("")
async def list_leads(campaign_id: UUID = None):
    """
    List all leads, optionally filtered by campaign.
    """
    query = supabase.table("leads").select("*")
    if campaign_id:
        query = query.eq("campaign_id", str(campaign_id))
    
    response = query.order("created_at", desc=True).execute()
    return response.data

@router.get("/{lead_id}")
async def get_lead(lead_id: UUID):
    """
    Get lead details.
    """
    response = supabase.table("leads").select("*").eq("id", str(lead_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return response.data[0]

@router.delete("/{lead_id}")
async def delete_lead(lead_id: UUID):
    """
    Delete a lead.
    """
    response = supabase.table("leads").delete().eq("id", str(lead_id)).execute()
    return {"status": "success"}
