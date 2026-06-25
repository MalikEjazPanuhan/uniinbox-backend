from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

class MessageBase(BaseModel):
    subject: Optional[str] = None
    body: str
    sender: Dict[str, Any]
    recipients: List[Dict[str, Any]]
    sent_at: datetime

class MessageCreate(MessageBase):
    channel_id: UUID
    persona_id: Optional[UUID] = None
    external_id: Optional[str] = None
    thread_external_id: Optional[str] = None

class MessageUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_flagged: Optional[bool] = None
    is_archived: Optional[bool] = None
    persona_id: Optional[UUID] = None
    summary: Optional[str] = None

class MessageResponse(MessageBase):
    id: UUID
    user_id: UUID
    channel_id: UUID
    persona_id: Optional[UUID] = None
    is_read: bool
    is_flagged: bool
    is_archived: bool
    importance_score: int
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    intent: Optional[str] = None
    entities: List[Dict[str, Any]] = []
    categories: List[str] = []
    ai_suggestions: List[Dict[str, Any]] = []
    ai_draft: Optional[str] = None
    created_at: datetime
    received_at: datetime
    
    class Config:
        from_attributes = True

class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
    total: int
    page: int
    size: int

class MessageReplyRequest(BaseModel):
    content: str
    persona_id: Optional[UUID] = None
