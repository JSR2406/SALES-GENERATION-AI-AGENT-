from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from typing import List, Dict, Any
from app.api.dependencies.database import get_supabase  # type: ignore
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{campaign_id}")
async def get_agent_logs(campaign_id: str, supabase=Depends(get_supabase)) -> Dict[str, Any]:
    """Retrieve all chronological execution logs for a specific campaign's AI agent."""
    try:
        response = supabase.table("agent_logs").select("*").eq("campaign_id", campaign_id).order("created_at").execute()
        return {"logs": response.data}
    except Exception as e:
        logger.error(f"Failed to fetch agent logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch agent logs")
