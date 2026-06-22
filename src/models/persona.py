from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from src.core.database import Base

class Persona(Base):
    __tablename__ = "personas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    
    name = Column(String(100), nullable=False)
    persona_type = Column(String(50), nullable=False)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    context = Column(JSON, nullable=False, default={
        "profession": "",
        "specialization": [],
        "company": "",
        "location": "",
        "experience_years": 0,
        "certifications": [],
        "languages": ["en"],
        "communication_style": "professional",
        "timezone": "UTC"
    })
    
    professional_details = Column(JSON, default=dict)
    knowledge_base = Column(JSON, default={
        "documents": [],
        "faqs": [],
        "common_phrases": [],
        "brand_voice": ""
    })
    
    ai_settings = Column(JSON, default={
        "draft_style": "balanced",
        "tone_modifiers": [],
        "signature": "",
        "auto_follow_up": False,
        "system_prompt_override": None
    })
    
    response_templates = Column(JSON, default=dict)
    active_channels = Column(JSON, default=list)
    
    generated_by_ai = Column(Boolean, default=False)
    generation_prompt = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships - Using STRING REFERENCES
    user = relationship("User", back_populates="personas")
    messages = relationship("Message", back_populates="persona")
    ai_actions = relationship("AIAction", back_populates="persona")

