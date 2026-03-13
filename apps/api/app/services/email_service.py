"""
Email Service — Extensible email sending via Resend, SendGrid, or SMTP.
Currently uses a mock sender. Replace with your provider of choice.
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class EmailProvider:
    """Base class for email providers."""

    async def send(self, to_email: str, subject: str, body: str, from_email: str = "agent@sales-ai.com") -> Dict[str, Any]:
        raise NotImplementedError

class MockEmailProvider(EmailProvider):
    """Mock provider for development — logs emails instead of sending."""

    async def send(self, to_email: str, subject: str, body: str, from_email: str = "agent@sales-ai.com") -> Dict[str, Any]:
        logger.info(f"📧 [MOCK] Email sent to {to_email}")
        logger.info(f"   Subject: {subject}")
        logger.info(f"   From: {from_email}")
        logger.info(f"   Body length: {len(body)} chars")
        return {
            "success": True,
            "provider": "mock",
            "message_id": f"mock_{hash(to_email + subject)}",
            "to": to_email,
            "subject": subject
        }

class ResendEmailProvider(EmailProvider):
    """
    Resend provider — uncomment and add `resend` to requirements.txt to activate.
    Set RESEND_API_KEY in your .env file.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        # import resend
        # resend.api_key = api_key

    async def send(self, to_email: str, subject: str, body: str, from_email: str = "agent@sales-ai.com") -> Dict[str, Any]:
        # import resend
        # params = {
        #     "from": from_email,
        #     "to": [to_email],
        #     "subject": subject,
        #     "html": f"<p>{body}</p>",
        # }
        # email = resend.Emails.send(params)
        # return {"success": True, "provider": "resend", "message_id": email["id"]}
        logger.warning("ResendEmailProvider: Not fully implemented. Using mock fallback.")
        return await MockEmailProvider().send(to_email, subject, body, from_email)


# ─── Factory ───
def get_email_provider(provider_name: str = "mock", api_key: Optional[str] = None) -> EmailProvider:
    """
    Factory to create email provider instances.
    Switch between providers by setting EMAIL_PROVIDER in .env.
    """
    providers = {
        "mock": lambda: MockEmailProvider(),
        "resend": lambda: ResendEmailProvider(api_key or ""),
    }
    
    creator = providers.get(provider_name, providers["mock"])
    return creator()

# Default instance
email_provider = get_email_provider("mock")
