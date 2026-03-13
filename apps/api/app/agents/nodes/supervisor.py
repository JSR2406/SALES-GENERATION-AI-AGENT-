import logging
from app.agents.state import AgentState

logger = logging.getLogger(__name__)

async def supervisor_node(state: AgentState) -> AgentState:
    """
    Supervisor determines the next best step deterministically based on flags.
    No LLM routing here - strictly rule-based.
    """
    logger.info(f"[{state['run_id']}] Supervisor checking state. Current Lead: {bool(state.get('current_lead'))}")
    
    # Check if we have leads but no current active lead
    if not state.get("current_lead") and not state.get("discovered_leads"):
        return {"next_action": "discover_leads", "current_step": "supervisor"}
        
    if state.get("discovered_leads") and not state.get("current_lead"):
        # Pop a lead (in a real system we'd manage a queue cursor)
        lead = state["discovered_leads"][0] # Just an example peek
        return {"current_lead": lead, "next_action": "enrich_lead", "current_step": "supervisor"}
        
    if state["current_lead"] and not state.get("enrichment_context"):
        return {"next_action": "enrich_lead", "current_step": "supervisor"}
        
    if state["current_lead"] and state.get("enrichment_context") and not state.get("qualification_result"):
        return {"next_action": "qualify_lead", "current_step": "supervisor"}
        
    if state.get("qualification_result"):
        # If score is low, we dump the lead
        if state["qualification_result"].get("score", 0) < 7.0: # Arbitrary threshold for demo
            return {"next_action": "persist_activity", "current_step": "supervisor"}
        # Otherwise, draft
        if not state.get("draft_email"):
            return {"next_action": "draft_email", "current_step": "supervisor"}
            
    if state.get("draft_email"):
        return {"next_action": "approval_gate", "current_step": "supervisor"}

    # Default fallback
    return {"next_action": "end", "current_step": "supervisor"}
