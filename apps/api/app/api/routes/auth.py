# apps/api/app/api/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.core.supabase import supabase
from app.core.security import get_password_hash, verify_password, create_access_token
from typing import Dict, Any

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None
    company_name: str = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(user_in: UserRegister):
    # Check if user exists
    existing = supabase.table("users").select("*").eq("email", user_in.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # Hash password
    hashed = get_password_hash(user_in.password)
    
    # Insert into Supabase
    user_data = {
        "email": user_in.email,
        "hashed_password": hashed,
        "full_name": user_in.full_name,
        "company_name": user_in.company_name,
        "is_active": True
    }
    
    response = supabase.table("users").insert(user_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    return {"status": "success", "user_id": response.data[0]["id"]}

@router.post("/login")
async def login(user_in: UserLogin):
    # Fetch user
    response = supabase.table("users").select("*").eq("email", user_in.email).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user = response.data[0]
    
    # Verify password
    if not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create token
    access_token = create_access_token(subject=user["id"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    }
