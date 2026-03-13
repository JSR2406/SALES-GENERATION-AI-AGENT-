import asyncio
from typing import List, Dict, Any
from app.services.providers.base import ILeadProvider, IEnrichmentProvider, IEmailProvider

class MockLeadProvider(ILeadProvider):
    async def discover_leads(self, query_params: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        await asyncio.sleep(1) # Simulate network jump
        return [
            {
                "full_name": "Alice Johnson",
                "first_name": "Alice",
                "last_name": "Johnson",
                "job_title": "VP of Engineering",
                "company_name": "TechFlow Systems",
                "company_domain": "techflow.example",
                "email": "alice@techflow.example",
                "source": "mock_apollo",
            },
            {
                "full_name": "Bob Smith",
                "first_name": "Bob",
                "last_name": "Smith",
                "job_title": "CTO",
                "company_name": "AI Startup Corp",
                "company_domain": "aistartup.example",
                "email": "bob@aistartup.example",
                "source": "mock_linkedin",
            }
        ][:limit]

class MockEnrichmentProvider(IEnrichmentProvider):
    async def enrich_lead(self, current_data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.5)
        return {
            "enrichment_summary": f"{current_data.get('company_name')} is a fast growing series-B startup actively seeking to streamline their data pipeline.",
            "linkedin_url": f"https://linkedin.com/in/{current_data.get('first_name', 'user').lower()}"
        }

class MockEmailProvider(IEmailProvider):
    async def send_email(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        await asyncio.sleep(0.5)
        # return standardized delivery dict
        return {
            "delivery_status": "sent",
            "provider_message_id": "mock_msg_" + recipient.split('@')[0],
            "error_message": None
        }
