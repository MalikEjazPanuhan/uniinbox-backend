from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.models.channel import Channel

class BaseConnector(ABC):
    """Base class for all channel connectors"""
    
    def __init__(self, channel: Channel):
        self.channel = channel
        self.config = channel.config
        self.tokens = {
            "access": channel.access_token,
            "refresh": channel.refresh_token
        }
    
    @abstractmethod
    async def fetch_messages(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch recent messages from the channel"""
        pass
    
    @abstractmethod
    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message through the channel"""
        pass
    
    @abstractmethod
    async def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read in the channel"""
        pass
    
    @abstractmethod
    async def reply_to_message(self, original_id: str, reply_content: str) -> Dict[str, Any]:
        """Reply to a specific message"""
        pass

