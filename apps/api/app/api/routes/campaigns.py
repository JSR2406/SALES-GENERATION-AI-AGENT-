# apps/api/app/api/routes/campaigns.py
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from typing import List, Dict, Any
from uuid import UUID
from app.core.supabase import supabase
from app.services.agent_service import AgentService

router = APIRouter()

@router.post("")
async def create_campaign(campaign_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Creates a new campaign in Supabase and triggers the AI agent background task.
    """
    # In a real app, we'd get user_id from token
    # For now, let's assume it's passed or use a default for dev
    if "user_id" not in campaign_data:
        campaign_data["user_id"] = "00000000-0000-0000-0000-000000000000"
    
    response = supabase.table("campaigns").insert(campaign_data).execute()
    
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create campaign")
    
    campaign = response.data[0]
    
    # Trigger background agent
    background_tasks.add_task(AgentService.run_campaign_pipeline, campaign["id"])
    
    return {"status": "success", "campaign": campaign}

@router.get("")
async def list_campaigns():
    """
    Lists all campaigns from Supabase.
    """
    response = supabase.table("campaigns").select("*").order("created_at", desc=True).execute()
    return response.data

@router.get("/{campaign_id}")
async def get_campaign(campaign_id: UUID):
    """
    Gets a single campaign profile.
    """
    response = supabase.table("campaigns").select("*").eq("id", str(campaign_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return response.data[0]

@router.get("/{campaign_id}/approvals")
async def get_pending_approvals(campaign_id: UUID):
    """
    Fetches leads and their drafted emails waiting for approval.
    """
    response = supabase.table("outreach_messages") \
        .select("*, leads(*)") \
        .eq("campaign_id", str(campaign_id)) \
        .eq("status", "pending_approval") \
        .execute()
        
    return response.data

@router.post("/approve/{message_id}")
async def approve_message(message_id: UUID):
    """
    Marks a message as approved and ready for sending.
    """
    response = supabase.table("outreach_messages") \
        .update({"status": "approved", "approved_by_user": True}) \
        .eq("id", str(message_id)) \
        .execute()
        
    return {"status": "success", "data": response.data}
