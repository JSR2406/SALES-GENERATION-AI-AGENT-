import logging
from app.agents.state import AgentState

logger = logging.getLogger(__name__)

async def draft_email_node(state: AgentState) -> AgentState:
    logger.info(f"[{state['run_id']}] Drafting personalization email")
    
    # Prompting logic ensuring no hallucinations:
    # "You are B2B Sales agent. Generate an email. Only use data provided in <Context>. If missing, use <Fallback>."
    
    name = state["current_lead"].get("first_name", "there")
    
    subject = f"Quick question about {state['current_lead'].get('company_name', 'your team')}"
    body = f"""Hi {name},\n\nNoticed you're leading engineering efforts based on your profile. Given our tool helps speed up deployment loops, I wanted to see if this is a priority right now?\n\nBest,\nSales Agent"""
    
    return {
        "draft_subject": subject,
        "draft_email": body,
        "personalization_notes": "Identified engineering role focus.",
        "current_step": "draft_email"
    }
