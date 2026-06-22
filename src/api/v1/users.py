from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.models.user import User
from src.schemas.user import UserResponse
from src.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me/update")
async def update_me(
    update_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    for key, value in update_data.items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return {"message": "User updated successfully"}

@router.get("/preferences")
async def get_preferences(current_user: User = Depends(get_current_user)):
    return current_user.preferences

@router.put("/preferences")
async def update_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.preferences = preferences
    db.commit()
    return {"message": "Preferences updated successfully"}

