# apps/api/app/services/providers/mock_email.py
import asyncio
import logging
from typing import Dict, Any
from app.services.providers.base import BaseEmailProvider
from app.models.enums import OutreachStatus

logger = logging.getLogger(__name__)

class MockEmailProvider(BaseEmailProvider):
    async def send_email(self, recipient_email: str, subject: str, body: str) -> Dict[str, Any]:
        """Mock behavior: simulates API network latency, logs directly to standard out, and returns Success."""
        await asyncio.sleep(0.5)
        
        logger.info(f"--- FAKE EMAIL DELIVERED TO {recipient_email} ---")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {body}")
        logger.info("-------------------------------------------------")
        
        return {
            "status": OutreachStatus.sent,
            "provider_message_id": f"mock_msg_{id(self)}",
            "error_message": None
        }
