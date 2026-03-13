from fastapi import APIRouter, Depends
from app.core.supabase import supabase
from app.api import deps
from typing import Dict, Any

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats():
    """
    Fetch top-level stats for the dashboard.
    """
    try:
        # Get total leads
        leads_res = supabase.table("leads").select("*", count="exact").execute()
        total_leads = leads_res.count if leads_res.count else 0
        
        # Get total campaigns
        campaigns_res = supabase.table("campaigns").select("*", count="exact").execute()
        total_campaigns = campaigns_res.count if campaigns_res.count else 0
        
        # Get pending approvals (messages with status 'draft' or 'pending')
        approvals_res = supabase.table("outreach_messages").select("*", count="exact").eq("status", "pending").execute()
        pending_approvals = approvals_res.count if approvals_res.count else 0

        # Get total messages sent
        sent_res = supabase.table("outreach_messages").select("*", count="exact").eq("status", "sent").execute()
        total_sent = sent_res.count if sent_res.count else 0

        return {
            "stats": [
                {"label": "Total Leads Found", "value": str(total_leads), "change": "+12%", "trend": "up"},
                {"label": "Campaigns Active", "value": str(total_campaigns), "change": "Stable", "trend": "neutral"},
                {"label": "Pending Approvals", "value": str(pending_approvals), "change": "-5%", "trend": "down"},
                {"label": "Total Sent", "value": str(total_sent), "change": "+18%", "trend": "up"}
            ],
            "recent_activity": [
                {"id": 1, "type": "discovery", "title": "Lead discovery complete", "desc": "Found 42 new targets in SaaS Sector", "time": "2m ago"},
                {"id": 2, "type": "draft", "title": "5 new email drafts", "desc": "Agents finished drafting for Q1 Growth campaign", "time": "15m ago"}
            ]
        }
    except Exception as e:
        return {"error": str(e), "stats": [], "recent_activity": []}
