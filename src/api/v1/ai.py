from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.user import User
from src.models.message import Message
from src.models.persona import Persona
from src.schemas.ai import (
    AISuggestionRequest, AISuggestionResponse,
    AIDraftRequest, AIDraftResponse,
    AISummarizeRequest, AISummarizeResponse
)
from src.services.ai_service import AIService
from src.api.deps import get_current_user

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/suggestions", response_model=AISuggestionResponse)
async def get_suggestions(
    request: AISuggestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify message and persona belong to user
    message = db.query(Message).filter(
        Message.id == request.message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    persona = db.query(Persona).filter(
        Persona.id == request.persona_id,
        Persona.user_id == current_user.id
    ).first()
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    ai_service = AIService()
    result = await ai_service.generate_reply_suggestions(
        message, persona, request.context
    )
    
    return result

@router.post("/draft", response_model=AIDraftResponse)
async def generate_draft(
    request: AIDraftRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    persona = db.query(Persona).filter(
        Persona.id == request.persona_id,
        Persona.user_id == current_user.id
    ).first()
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    ai_service = AIService()
    draft = await ai_service.generate_draft(
        request.model_dump(), persona
    )
    
    return {
        "draft": draft,
        "persona_name": persona.name,
        "model_used": ai_service.default_model
    }

@router.post("/summarize", response_model=AISummarizeResponse)
async def summarize_thread(
    request: AISummarizeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    persona = db.query(Persona).filter(
        Persona.id == request.persona_id,
        Persona.user_id == current_user.id
    ).first()
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    # Get thread messages
    messages = db.query(Message).filter(
        Message.thread_id == request.thread_id,
        Message.user_id == current_user.id
    ).order_by(Message.sent_at).all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    ai_service = AIService()
    summary = await ai_service.summarize_thread(messages, persona)
    
    return {
        "summary": summary,
        "key_points": ["Key point 1", "Key point 2"],
        "action_items": ["Action item 1", "Action item 2"]
    }

