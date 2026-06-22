from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime

from src.models.message import Message
from src.models.channel import Channel
from src.models.persona import Persona
from src.models.user import User
from src.connectors.gmail import GmailConnector
from src.connectors.slack import SlackConnector
from src.connectors.outlook import OutlookConnector

class MessageService:
    def __init__(self, db: Session):
        self.db = db
    
    def process_incoming_message(self, channel_id: uuid.UUID, raw_message: Dict[str, Any]) -> Message:
        """Process and store an incoming message from a channel"""
        
        # Check if message already exists
        existing = self.db.query(Message).filter(
            Message.channel_id == channel_id,
            Message.external_id == raw_message.get("external_id")
        ).first()
        
        if existing:
            return existing
        
        # Get channel and user
        channel = self.db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise ValueError(f"Channel {channel_id} not found")
        
        # Create message
        message = Message(
            user_id=channel.user_id,
            channel_id=channel_id,
            external_id=raw_message.get("external_id"),
            thread_external_id=raw_message.get("thread_id"),
            subject=raw_message.get("subject", ""),
            body=raw_message.get("body", ""),
            body_html=raw_message.get("body_html", ""),
            sender=raw_message.get("from", {}),
            recipients=raw_message.get("to", []),
            sent_at=raw_message.get("sent_at", datetime.utcnow()),
            is_read=raw_message.get("is_read", False),
            attachments=raw_message.get("attachments", [])
        )
        
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        return message
    
    async def reply_to_message(
        self,
        message_id: uuid.UUID,
        content: str,
        persona_id: Optional[uuid.UUID] = None,
        user_id: Optional[uuid.UUID] = None
    ) -> Dict[str, Any]:
        """Reply to a message through its channel"""
        
        # Get original message
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if not message:
            raise ValueError(f"Message {message_id} not found")
        
        # Get channel
        channel = self.db.query(Channel).filter(Channel.id == message.channel_id).first()
        if not channel:
            raise ValueError(f"Channel {message.channel_id} not found")
        
        # Get persona if provided
        persona = None
        if persona_id:
            persona = self.db.query(Persona).filter(Persona.id == persona_id).first()
        
        # Get appropriate connector
        connector = self._get_connector(channel)
        
        # Send reply
        reply_data = {
            "to": [message.sender.get("email", "")],
            "subject": f"Re: {message.subject}",
            "body": content,
            "thread_id": message.thread_external_id
        }
        
        result = await connector.send_message(reply_data)
        
        if result.get("success"):
            # Update original message
            message.replied_at = datetime.utcnow()
            if persona_id:
                message.persona_id = persona_id
            self.db.commit()
        
        return {
            "success": result.get("success", False),
            "message_id": str(message.id),
            "reply_to": message.sender.get("email", ""),
            "persona": persona.name if persona else None
        }
    
    def _get_connector(self, channel: Channel):
        """Get the appropriate connector for a channel"""
        if channel.channel_type == "gmail":
            return GmailConnector(channel)
        elif channel.channel_type == "slack":
            return SlackConnector(channel)
        elif channel.channel_type == "outlook":
            return OutlookConnector(channel)
        else:
            raise ValueError(f"Unsupported channel type: {channel.channel_type}")
        
