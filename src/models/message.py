from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from src.core.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    persona_id = Column(UUID(as_uuid=True), ForeignKey("personas.id", ondelete="SET NULL"))
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"))
    
    external_id = Column(String(255), nullable=True)
    thread_external_id = Column(String(255), nullable=True)
    
    subject = Column(String(500), nullable=True)
    body = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    
    sender = Column(JSON, nullable=False)
    recipients = Column(JSON, nullable=False)
    
    is_read = Column(Boolean, default=False)
    is_flagged = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    importance_score = Column(Integer, default=0)
    
    sentiment = Column(String(50), nullable=True)
    intent = Column(String(100), nullable=True)
    entities = Column(JSON, default=list)
    categories = Column(JSON, default=list)
    
    in_reply_to = Column(UUID(as_uuid=True), nullable=True)
    thread_id = Column(UUID(as_uuid=True), nullable=True)
    
    sent_at = Column(DateTime(timezone=True), nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    replied_at = Column(DateTime(timezone=True), nullable=True)
    
    ai_suggestions = Column(JSON, default=list)
    ai_draft = Column(Text, nullable=True)
    ai_draft_generated_at = Column(DateTime(timezone=True), nullable=True)
    
    attachments = Column(JSON, default=list)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships - Using STRING REFERENCES
    user = relationship("User", back_populates="messages")
    persona = relationship("Persona", back_populates="messages")
    channel = relationship("Channel", back_populates="messages")

