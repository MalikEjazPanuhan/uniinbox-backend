from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from src.core.database import get_db
from src.models.user import User
from src.models.message import Message
from src.schemas.message import MessageResponse, MessageListResponse, MessageReplyRequest
from src.api.deps import get_current_user
from src.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("/", response_model=MessageListResponse)
async def get_messages(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    channel_id: Optional[uuid.UUID] = None,
    persona_id: Optional[uuid.UUID] = None,
    is_read: Optional[bool] = None,
    is_flagged: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Message).filter(Message.user_id == current_user.id)
    
    if channel_id:
        query = query.filter(Message.channel_id == channel_id)
    if persona_id:
        query = query.filter(Message.persona_id == persona_id)
    if is_read is not None:
        query = query.filter(Message.is_read == is_read)
    if is_flagged is not None:
        query = query.filter(Message.is_flagged == is_flagged)
    if search:
        query = query.filter(
            Message.subject.ilike(f"%{search}%") | 
            Message.body.ilike(f"%{search}%")
        )
    
    total = query.count()
    messages = query.offset((page - 1) * size).limit(size).all()
    
    return {
        "messages": messages,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message

@router.put("/{message_id}/read")
async def mark_as_read(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    message.read_at = db.func.now()
    db.commit()
    
    return {"message": "Marked as read"}

@router.put("/{message_id}/unread")
async def mark_as_unread(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = False
    message.read_at = None
    db.commit()
    
    return {"message": "Marked as unread"}

@router.put("/{message_id}/flag")
async def toggle_flag(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_flagged = not message.is_flagged
    db.commit()
    
    return {"message": f"Flagged: {message.is_flagged}"}

@router.post("/{message_id}/reply")
async def reply_to_message(
    message_id: uuid.UUID,
    reply_data: MessageReplyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    service = MessageService(db)
    result = await service.reply_to_message(
        message_id,
        reply_data.content,
        reply_data.persona_id,
        current_user.id
    )
    
    return result

@router.get("/thread/{thread_id}")
async def get_thread(
    thread_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        Message.thread_id == thread_id,
        Message.user_id == current_user.id
    ).order_by(Message.sent_at).all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    return {"thread": messages, "count": len(messages)}

