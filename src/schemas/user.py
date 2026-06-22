from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    company: Optional[str] = None
    job_title: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    is_enterprise: bool
    created_at: datetime
    preferences: Dict[str, Any] = {}
    ai_settings: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenRefresh(BaseModel):
    refresh_token: str

