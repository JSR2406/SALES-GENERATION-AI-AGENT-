# apps/api/app/api/router.py
from fastapi import APIRouter  # type: ignore
from app.api.routes import auth, campaigns, leads, dashboard, webhooks, agent_logs  # type: ignore

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(agent_logs.router, prefix="/agent-logs", tags=["agent-logs"])
# More modules (outreach, dashboard) will go here over time
