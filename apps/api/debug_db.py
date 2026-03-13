import os
from dotenv import load_dotenv
from supabase import create_client
from uuid import uuid4

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

u_id = str(uuid4())
c_id = str(uuid4())

print(f"User: {u_id}")
print(f"Campaign: {c_id}")

try:
    print("Inserting user...")
    u_res = supabase.table("users").insert({
        "id": u_id,
        "email": f"test_{u_id[:8]}@example.com",
        "hashed_password": "test",
        "full_name": "Test"
    }).execute()
    print("User inserted.")
    
    print("Inserting campaign...")
    c_res = supabase.table("campaigns").insert({
        "id": c_id,
        "user_id": u_id,
        "campaign_name": "Minimal Test",
        "status": "draft",
        "sending_mode": "manual_approval"
    }).execute()
    print("Campaign inserted.")
except Exception as e:
    print(f"Error: {e}")
