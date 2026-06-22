from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from src.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    
    default_persona_id = Column(UUID(as_uuid=True), nullable=True)
    active_personas = Column(JSON, default=list)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_enterprise = Column(Boolean, default=False)
    encryption_key_encrypted = Column(String(500), nullable=True)
    
    preferences = Column(JSON, default=dict)
    ai_settings = Column(JSON, default={
        "auto_draft": False,
        "auto_summarize": True,
        "tone": "professional",
        "language": "en"
    })
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships - Using STRING REFERENCES (no imports needed)
    personas = relationship("Persona", back_populates="user", cascade="all, delete-orphan")
    channels = relationship("Channel", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user")
    ai_actions = relationship("AIAction", back_populates="user")  # ← String reference

    