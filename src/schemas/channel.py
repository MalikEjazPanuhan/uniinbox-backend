from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

class ChannelBase(BaseModel):
    channel_type: str
    channel_name: str
    config: Optional[Dict[str, Any]] = {}
    sync_enabled: bool = True
    sync_frequency: int = 60
    monitored_folders: List[str] = ["INBOX", "IMPORTANT"]
    excluded_folders: List[str] = ["SPAM", "TRASH"]

class ChannelCreate(ChannelBase):
    pass

class ChannelUpdate(BaseModel):
    channel_name: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    sync_enabled: Optional[bool] = None
    sync_frequency: Optional[int] = None
    monitored_folders: Optional[List[str]] = None
    excluded_folders: Optional[List[str]] = None

class ChannelResponse(ChannelBase):
    id: UUID
    user_id: UUID
    is_active: bool
    last_sync: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChannelAuthResponse(BaseModel):
    auth_url: str
    channel_type: str

