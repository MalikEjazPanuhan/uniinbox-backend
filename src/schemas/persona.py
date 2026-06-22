from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

class PersonaBase(BaseModel):
    name: str
    persona_type: str
    context: Dict[str, Any]
    professional_details: Optional[Dict[str, Any]] = {}
    ai_settings: Optional[Dict[str, Any]] = {}
    is_default: bool = False

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    professional_details: Optional[Dict[str, Any]] = None
    ai_settings: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class PersonaResponse(PersonaBase):
    id: UUID
    user_id: UUID
    is_active: bool
    generated_by_ai: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OnboardingData(BaseModel):
    full_name: str
    job_title: str
    company: str
    industry: str
    specialization: List[str] = []
    experience_years: int = 0
    communication_style: str = "professional"
    primary_audience: str
    certifications: List[str] = []
    languages: List[str] = ["en"]
    timezone: str = "UTC"
    preferences: Dict[str, Any] = {}

class PersonaGenerationRequest(BaseModel):
    onboarding_data: OnboardingData
    custom_instructions: Optional[str] = None

