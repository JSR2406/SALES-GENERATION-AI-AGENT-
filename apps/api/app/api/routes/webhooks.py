from fastapi import APIRouter, HTTPException, Depends  # type: ignore
from pydantic import BaseModel, Field  # type: ignore
from typing import Optional
from enum import Enum
from langchain_anthropic import ChatAnthropic  # type: ignore
from langchain_core.messages import HumanMessage  # type: ignore
from app.core.config import settings  # type: ignore
from app.api.dependencies.database import get_supabase  # type: ignore
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=settings.ANTHROPIC_API_KEY)

class ReplyCategory(str, Enum):
    interested = "interested"
    not_interested = "not_interested"
    ask_later = "ask_later"
    bounced = "bounced"
    out_of_office = "out_of_office"
    neutral = "neutral"

class ReplyClassification(BaseModel):
    classification: ReplyCategory = Field(description="Categorization of the reply.")
    sentiment: str = Field(description="Positive, Negative, or Neutral sentiment analysis of the reply.")
    extracted_intent: str = Field(description="A brief 1-sentence summary of what the prospect wants next.")

class EmailWebhookPayload(BaseModel):
    from_email: str
    subject: str
    text: str

@router.post("/email")
async def handle_email_webhook(payload: EmailWebhookPayload, supabase=Depends(get_supabase)):
    """
    Receives an incoming email reply, associates it with a lead, 
    classifies the intent using AI, and saves the reply to the database.
    """
    logger.info(f"📬 Received webhook reply from {payload.from_email}")
    
    # 1. Find the associated lead
    leads_resp = supabase.table("leads").select("*").eq("email", payload.from_email).execute()
    leads = leads_resp.data
    
    if not leads:
        logger.warning(f"⚠️ Webhook: No lead found matching email {payload.from_email}")
        return {"status": "ignored", "reason": "no_matching_lead"}
    
    lead = leads[0]
    lead_id = lead["id"]
    
    # 2. Classify reply using Langchain & Claude
    prompt = f"""
    Analyze the following email reply from a B2B sales prospect.
    Prospect Email: {payload.from_email}
    Subject: {payload.subject}
    Body:
    {payload.text}
    
    Classify the overarching intent of the email, extract the general sentiment, and concisely state what the prospect wants.
    """
    
    try:
        structured_llm = llm.with_structured_output(ReplyClassification)
        classification_result: ReplyClassification = await structured_llm.ainvoke([HumanMessage(content=prompt)])  # type: ignore
        logger.info(f"🧠 AI Classification for {payload.from_email}: {classification_result.classification.value}")
    except Exception as e:
        logger.error(f"❌ Failed to classify reply: {e}")
        return {"status": "error", "message": "Failed to classify reply"}
    
    # 3. Store the reply in the DB
    reply_data = {
        "lead_id": lead_id,
        "outreach_message_id": lead_id, # Fallback, ideally provided by thread-id
        "provider_thread_id": None,
        "reply_text": payload.text,
        "classification": classification_result.classification.value,
        "sentiment": classification_result.sentiment,
        "extracted_intent": classification_result.extracted_intent,
        "received_at": datetime.utcnow().isoformat()
    }
    
    try:
        supabase.table("replies").insert(reply_data).execute()
        
        # 4. Optional: Update lead status based on classification
        if classification_result.classification == ReplyCategory.interested:
            supabase.table("leads").update({"status": "replied_interested"}).eq("id", lead_id).execute()
        elif classification_result.classification == ReplyCategory.not_interested:
            supabase.table("leads").update({"status": "replied_rejected"}).eq("id", lead_id).execute()
        else:
            supabase.table("leads").update({"status": "replied"}).eq("id", lead_id).execute()
            
        return {"status": "success", "classification": classification_result.classification.value}
    except Exception as e:
        logger.error(f"❌ Failed to process webhook data in Supabase: {e}")
        raise HTTPException(status_code=500, detail="Database Error")
