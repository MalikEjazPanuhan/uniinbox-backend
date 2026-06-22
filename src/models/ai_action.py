from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from src.core.database import Base

class AIAction(Base):
    __tablename__ = "ai_actions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    persona_id = Column(UUID(as_uuid=True), ForeignKey("personas.id", ondelete="SET NULL"))
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="SET NULL"))
    
    action_type = Column(String(50), nullable=False)
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=True)
    
    status = Column(String(50), default="pending")
    error = Column(Text, nullable=True)
    
    model_used = Column(String(100), nullable=True)
    tokens_used = Column(Integer, default=0)
    processing_time_ms = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships - Using STRING REFERENCES
    user = relationship("User", back_populates="ai_actions")
    persona = relationship("Persona", back_populates="ai_actions")

    