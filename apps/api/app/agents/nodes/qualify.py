import logging
from app.agents.state import AgentState

# To prevent hallucinations, we use structured output logic here in a real scenario
# e.g., using Instructor or LangChain `with_structured_output`

logger = logging.getLogger(__name__)

async def qualify_lead_node(state: AgentState) -> AgentState:
    logger.info(f"[{state['run_id']}] Qualifying lead against ICP")
    
    # Mock LLM evaluation logic.
    # In reality: prompt LLM with state["campaign_data"]["target_icp"] and state["enrichment_context"]
    # Require JSON output {"score": float, "reason": str}
    
    # For MVP logic
    email = state["current_lead"].get("email", "")
    score = 9.0 if "techflow" in email else 6.0
    reason = "Strong match for SaaS products" if score > 7.0 else "Outside of ICP parameters"
    
    result = {"score": score, "reason": reason}
    
    return {
        "qualification_result": result,
        "current_step": "qualify_lead",
        "logs": [{"action": "qualify", "status": "success", "metadata": result}]
    }
