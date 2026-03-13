# apps/api/app/services/providers/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLeadScraper(ABC):
    @abstractmethod
    async def discover_leads(self, target_industries: List[str], target_titles: List[str], target_locations: List[str], limit: int) -> List[Dict[str, Any]]:
        """Fetch leads matching targeting criteria."""
        pass

class BaseEmailProvider(ABC):
    @abstractmethod
    async def send_email(self, recipient_email: str, subject: str, body: str) -> Dict[str, Any]:
        """Dispatch email and return delivery metadata (status, message_id, etc)."""
        pass
