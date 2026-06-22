from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from src.core.database import Base

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    
    channel_type = Column(String(50), nullable=False)
    channel_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expiry = Column(DateTime(timezone=True), nullable=True)
    
    config = Column(JSON, default=dict)
    channel_metadata = Column(JSON, default=dict)
    
    sync_enabled = Column(Boolean, default=True)
    sync_frequency = Column(Integer, default=60)
    last_sync = Column(DateTime(timezone=True))
    
    monitored_folders = Column(JSON, default=["INBOX", "IMPORTANT"])
    excluded_folders = Column(JSON, default=["SPAM", "TRASH"])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships - Using STRING REFERENCES
    user = relationship("User", back_populates="channels")
    messages = relationship("Message", back_populates="channel")

