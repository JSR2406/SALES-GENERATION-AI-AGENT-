import logging
import asyncio
from typing import Dict, Any, List

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_anthropic import ChatAnthropic

from app.core.config import settings
from app.agents.state import AgentState
from app.agents.prompts import qualify_agent_prompt, draft_agent_prompt
from app.agents.schemas import LeadQualificationResult, DraftedEmail
from app.services.providers.mock_scraper import MockScraperProvider
from app.services.providers.mock_email import MockEmailProvider

logger = logging.getLogger(__name__)

llm = ChatAnthropic(api_key=settings.ANTHROPIC_API_KEY, model_name="claude-3-5-sonnet-20241022", temperature=0.1)
mock_scraper = MockScraperProvider()
mock_email = MockEmailProvider()

async def supervisor_node(state: AgentState) -> dict:
    """Supervises the progress and determines next route based on state context."""
    logger.info("--- SUPERVISOR EVALUATING STATE ---")
    
    if state["errors"] and len(state["errors"]) > 2:
        return {"next_action": "failure", "routing_status": "error"}
        
    if not state.get("discovered_leads") and not state.get("current_lead"):
        # Initial step
        return {"next_action": "discover_leads"}
        
    if state.get("discovered_leads") and not state.get("current_lead"):
        # Select next lead
        return {"next_action": "enrich_lead"}
        
    # Standard linear path for a lead
    if state.get("current_lead") and not state.get("qualification_result"):
        return {"next_action": "qualify_lead"}
        
    if state.get("qualification_result") and not state.get("draft_email"):
        if state["qualification_result"].get("score", 0) > 7.0:
            return {"next_action": "draft_email"}
        else:
            # Lead is unqualified, skip them
            return {
                "next_action": "enrich_lead", 
                "logs": state.get("logs", []) + [f"Lead {state['current_lead'].get('full_name')} rejected (Score {state['qualification_result'].get('score')})"]
            }
            
    if state.get("draft_email"):
        # We have a drafted email
        if state["sending_mode"] == "auto_send":
            return {"next_action": "send_email"}
        else:
            return {"next_action": "approval_gate"}
            
    return {"next_action": "end"}

async def discover_leads_node(state: AgentState) -> dict:
    """Invokes scraper to find leads matching the ICP."""
    logger.info("--- DISCOVERING LEADS ---")
    icp = state["campaign_data"]["target_icp"]
    
    leads = await mock_scraper.discover_leads(
        target_industries=icp.get("industries", []),
        target_titles=icp.get("roles", []),
        target_locations=[],
        limit=2
    )
    
    return {"discovered_leads": leads, "next_action": "supervisor"}

async def enrich_lead_node(state: AgentState) -> dict:
    """Pops a lead from the discovery list and 'enriches' it."""
    logger.info("--- ENRICHING LEAD ---")
    leads = state.get("discovered_leads", [])
    
    if not leads:
        logger.info("No leads left to process.")
        return {"next_action": "end"}
        
    # Pop the first lead
    current_lead = leads.pop(0)
    
    # In a real app, this simulates an API call to Apollo/Clearbit
    enrichment_context = {
        "recent_news": "Recently raised Series A",
        "tech_stack": ["React", "Python"]
    }
    
    return {
        "discovered_leads": leads, 
        "current_lead": current_lead, 
        "enrichment_context": enrichment_context,
        "qualification_result": None, # Reset for new lead
        "draft_email": None,
        "next_action": "supervisor"
    }

async def qualify_lead_node(state: AgentState) -> dict:
    """LLM determines if the lead perfectly matches the ICP."""
    logger.info("--- QUALIFYING LEAD ---")
    
    prompt = qualify_agent_prompt.format(
        target_icp=str(state["target_icp"]),
        lead_data=str(state["current_lead"])
    )
    
    # Note: Anthropic models easily support structured outputs with langchain via with_structured_output
    if not settings.ANTHROPIC_API_KEY:
        # Mock result for local dev if API key is missing
        return {"qualification_result": {"score": 8.5, "reason": "Mock qualification."}}
        
    try:
        structured_llm = llm.with_structured_output(LeadQualificationResult)
        result = await structured_llm.ainvoke([HumanMessage(content=prompt)])
        
        return {
            "qualification_result": {"score": result.score, "reason": result.reason},
            "next_action": "supervisor"
        }
    except Exception as e:
        logger.error(f"Qualification failed: {e}")
        return {"errors": [str(e)], "next_action": "supervisor"}

async def draft_email_node(state: AgentState) -> dict:
    """LLM drafts a hyper-personalized email based on strict constraints."""
    logger.info("--- DRAFTING EMAIL ---")
    
    lead = state["current_lead"]
    prompt = draft_agent_prompt.format(
        value_proposition=state["user_value_prop"],
        offer_summary=state["offer_summary"],
        lead_name=lead.get("full_name"),
        lead_title=lead.get("job_title"),
        company_name=lead.get("company_name"),
        company_info=lead.get("company_description")
    )
    
    if not settings.ANTHROPIC_API_KEY:
        # Mock result
        return {"draft_subject": "Mock Subject", "draft_email": "Mock Body context ...", "next_action": "supervisor"}

    try:
        structured_llm = llm.with_structured_output(DraftedEmail)
        result = await structured_llm.ainvoke([HumanMessage(content=prompt)])
        
        return {
            "draft_subject": result.subject,
            "draft_email": result.body,
            "next_action": "supervisor" # Returns control to supervisor
        }
    except Exception as e:
        logger.error(f"Drafting failed: {e}")
        return {"errors": [str(e)], "next_action": "supervisor"}

async def approval_gate_node(state: AgentState) -> dict:
    """A stopping node to wait for human approval if manual mode is enabled."""
    logger.info("--- WAITING AT APPROVAL GATE ---")
    # In LangGraph, we actually pause execution here (using Command or interrupts in newer versions, or breaking the graph).
    # Since we are designing a background worker, if sending_mode is manual_approval, we persist the state and END execution.
    # The user API will trigger the continuation later.
    return {"approval_required": True}
    
async def send_email_node(state: AgentState) -> dict:
    """Dispatches the email securely using an Email Provider."""
    logger.info("--- SENDING EMAIL ---")
    lead = state["current_lead"]
    
    await mock_email.send_email(
        recipient_email=lead.get("email", "fake@example.com"),
        subject=state.get("draft_subject", "No subject"),
        body=state.get("draft_email", "No body")
    )
    
    return {"send_decision": True, "next_action": "enrich_lead"} # loops to next lead

async def failure_handler_node(state: AgentState) -> dict:
    logger.error("--- HANDLING FAILURE ---")
    # Write failing states to DB, alert user, halt campaign
    return {"logs": state.get("logs", []) + ["Graph halted due to maximum error threshold."]}
