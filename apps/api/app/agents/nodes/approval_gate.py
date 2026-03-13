import logging
from app.agents.state import AgentState

logger = logging.getLogger(__name__)

async def approval_gate_node(state: AgentState) -> AgentState:
    """
    Decides if we pause for manual UI approval or if we jump straight to send_email_node
    based on campaign settings.
    """
    logger.info(f"[{state['run_id']}] Evaluating approval gate.")
    
    mode = state["campaign_data"].get("sending_mode", "manual_approval")
    
    if mode == "auto_send":
        return {"send_decision": True, "approval_required": False, "next_action": "send_email", "current_step": "approval_gate"}
    else:
        # Requires user intervention via UI.
        # Returning next_action='persist_activity' or similar to just store state and pause execution.
        return {"send_decision": False, "approval_required": True, "next_action": "persist_activity", "current_step": "approval_gate"}
