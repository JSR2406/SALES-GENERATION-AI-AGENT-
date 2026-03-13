import logging
from app.agents.state import AgentState
from app.services.providers.mocks import MockEnrichmentProvider

logger = logging.getLogger(__name__)

async def enrich_lead_node(state: AgentState) -> AgentState:
    logger.info(f"[{state['run_id']}] Enriching lead {state['current_lead'].get('email')}")
    provider = MockEnrichmentProvider()
    
    enrichment_data = await provider.enrich_lead(state["current_lead"])
    
    return {
        "enrichment_context": enrichment_data.get("enrichment_summary", ""),
        "current_step": "enrich_lead"
    }
