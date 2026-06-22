from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.database import get_db
from src.models.user import User
from src.models.persona import Persona
from src.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse
from src.services.persona_service import PersonaService
from src.api.deps import get_current_user

router = APIRouter(prefix="/personas", tags=["personas"])

@router.post("/", response_model=PersonaResponse)
async def create_persona(
    persona_data: PersonaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = PersonaService(db)
    return service.create_persona(current_user.id, persona_data)

@router.get("/", response_model=List[PersonaResponse])
async def get_personas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Persona).filter(
        Persona.user_id == current_user.id,
        Persona.is_active == True
    ).all()

@router.get("/{persona_id}", response_model=PersonaResponse)
async def get_persona(
    persona_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    persona = db.query(Persona).filter(
        Persona.id == persona_id,
        Persona.user_id == current_user.id
    ).first()
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    return persona

@router.put("/{persona_id}", response_model=PersonaResponse)
async def update_persona(
    persona_id: uuid.UUID,
    persona_data: PersonaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = PersonaService(db)
    return service.update_persona(current_user.id, persona_id, persona_data)

@router.delete("/{persona_id}")
async def delete_persona(
    persona_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = PersonaService(db)
    service.delete_persona(current_user.id, persona_id)
    return {"message": "Persona deleted successfully"}

@router.post("/{persona_id}/set-default")
async def set_default_persona(
    persona_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = PersonaService(db)
    service.set_default_persona(current_user.id, persona_id)
    return {"message": "Default persona set successfully"}

