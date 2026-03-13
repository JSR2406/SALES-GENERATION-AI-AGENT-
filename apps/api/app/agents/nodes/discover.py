import logging
from app.agents.state import AgentState
from app.services.providers.mocks import MockLeadProvider

logger = logging.getLogger(__name__)

async def discover_leads_node(state: AgentState) -> AgentState:
    """Invokes the external provider to fetch candidate leads."""
    logger.info(f"[{state['run_id']}] Discovering leads...")
    provider = MockLeadProvider()
    
    # We should pull parameters from state['campaign_data']
    leads = await provider.discover_leads({}, limit=2) 
    
    log_entry = {
         "action": "discover_leads",
         "status": "success",
         "metadata": f"Found {len(leads)} leads"
    }
    
    return {
        "discovered_leads": leads,
        "current_step": "discover_leads",
        "logs": [log_entry]
    }
