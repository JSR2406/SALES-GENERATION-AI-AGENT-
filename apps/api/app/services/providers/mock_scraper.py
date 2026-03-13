# apps/api/app/services/providers/mock_scraper.py
import asyncio
from typing import List, Dict, Any
from app.services.providers.base import BaseLeadScraper

class MockScraperProvider(BaseLeadScraper):
    async def discover_leads(
        self, target_industries: List[str], target_titles: List[str], target_locations: List[str], limit: int
    ) -> List[Dict[str, Any]]:
        """Mock behavior: simulates scraping delay and returns structured ICP leads."""
        await asyncio.sleep(1.0)
        
        industry = target_industries[0] if target_industries else "Software"
        title = target_titles[0] if target_titles else "Founder"
        
        leads = [
            {
                "full_name": "Erlich Bachman",
                "email": "erlich@aviato.example.com",
                "company_name": "Aviato",
                "job_title": title,
                "industry": industry,
                "company_description": "We are a transportation software company focused on logistics and finding hotels quickly."
            },
            {
                "full_name": "Richard Hendricks",
                "email": "richard@piedpiper.example.com",
                "company_name": "Pied Piper",
                "job_title": title,
                "industry": industry,
                "company_description": "We built a middle-out compression algorithm that works flawlessly for video and heavy data processing."
            }
        ]
        
        return leads[:limit]
