# apps/api/app/agents/schemas.py
from pydantic import BaseModel, Field

class LeadQualificationResult(BaseModel):
    score: float = Field(..., description="A score from 0.0 to 10.0 indicating how well the lead fits the target ICP. 10 is perfect.")
    reason: str = Field(..., description="A concise 1-2 sentence justification on why this score was assigned based ONLY on the evidence provided.")

class DraftedEmail(BaseModel):
    subject: str = Field(..., description="The highly personalized subject line of the email.")
    body: str = Field(..., description="The full body of the cold email tailored strictly to the lead's provided context and the target value prop.")
    confidence_score: float = Field(..., description="A confidence factor from 0.0 to 1.0 indicating how confident the model is that it avoided hallucination.")
