from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
import uuid

from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Simplified mock auth dependency for local development since we don't have a real JWT implementation configured yet.
# In a real app we decode the JWT, verify the signature, and extract the user.
async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    # MOCK implementation: Return a default user
    # Try linking to an existing user, else create a dummy
    result = await db.execute(select(User).limit(1))
    user = result.scalars().first()
    
    if not user:
        # Provide a fallback context for prototyping
        user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            email="admin@example.com",
            hashed_password="fake",
            full_name="Mock Admin"
        )
        # Avoid saving dummy user if we aren't handling real migrations yet properly
    
    return user
