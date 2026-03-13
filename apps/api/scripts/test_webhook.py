import os
import sys
import httpx
from dotenv import load_dotenv
from supabase import create_client, Client
import random

# Ensure we're running from the right directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", ".env")
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY is missing from environment variables.")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
API_URL = "http://localhost:8000/webhooks/email"

def create_mock_lead() -> str:
    """Creates a mock user, campaign, and lead in the DB."""
    # 1. Ensure User exists
    user_resp = supabase.table("users").select("id").limit(1).execute()
    if not user_resp.data:
        print("ℹ️ Creating test user...")
        from uuid import uuid4
        user_id = str(uuid4())
        try:
            supabase.table("users").insert({
                "id": user_id,
                "email": "test@example.com",
                "hashed_password": "fake",
                "full_name": "Test User"
            }).execute()
        except Exception as e:
            print(f"❌ User Creation Error: {e}")
            sys.exit(1)
    else:
        user_id = user_resp.data[0]['id']

    # 2. Ensure Campaign exists
    campaign_resp = supabase.table("campaigns").select("id").limit(1).execute()
    if not campaign_resp.data:
        from uuid import uuid4
        campaign_id = str(uuid4())
        print(f"ℹ️ Creating test campaign {campaign_id}...")
        try:
            res = supabase.table("campaigns").insert({
                "id": campaign_id,
                "user_id": user_id,
                "campaign_name": "Test Campaign",
                "target_industries": ["Software"],
                "status": "running",
                "sending_mode": "manual_approval"
            }).execute()
        except Exception as e:
            import json
            print(f"❌ Campaign Creation Error Details: {str(e)}")
            sys.exit(1)
    else:
        campaign_id = campaign_resp.data[0]['id']
        
    unique_id = random.randint(1000, 9999)
    email = f"john.doe.test.{unique_id}@example.com"
    from uuid import uuid4
    lead_id = str(uuid4())
    
    lead_data = {
        "id": lead_id,
        "campaign_id": campaign_id,
        "email": email,
        "full_name": "John Doe",
        "company_name": "Test Company Inc.",
        "status": "contacted" # Simulating we've sent them a message
    }
    
    try:
        supabase.table("leads").insert(lead_data).execute()
        print(f"✅ Created mock lead: {email} for campaign {campaign_id}")
    except Exception as e:
        print(f"❌ Lead Creation Error: {e}")
        sys.exit(1)
        
    return email

def test_reply(email: str, subject: str, text: str):
    print(f"\n📨 Simulating webhook send for: {email}...")
    payload = {
        "from_email": email,
        "subject": subject,
        "text": text
    }
    
    try:
        response = httpx.post(API_URL, json=payload, timeout=30.0)
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 Response Body: {response.json()}")
        
        # Verify DB Status changed
        resp = supabase.table("leads").select("status").eq("email", email).execute()
        if len(resp.data) > 0:
            print(f"🔍 Verified Lead Status via DB: {resp.data[0]['status']}")
    except Exception as e:
        print(f"❌ Failed to send request: {e}")

if __name__ == "__main__":
    test_email = create_mock_lead()
    
    print("\n--- TEST 1: Interested Reply ---")
    test_reply(
        test_email, 
        "Re: Your outreach", 
        "Thanks for reaching out! We are actually looking into updating our software stacks. Do you have time for a brief 15min sync this Thursday?"
    )
    
    print("\n--- TEST 2: Not Interested Reply ---")
    test_email2 = create_mock_lead()
    test_reply(
        test_email2, 
        "Re: Your outreach", 
        "Please remove me from your list. We just signed a 2-year contract with your competitor."
    )
