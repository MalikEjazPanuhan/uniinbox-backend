from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import Optional
import uuid

from src.models.persona import Persona
from src.models.user import User
from src.schemas.persona import PersonaCreate, PersonaUpdate

class PersonaService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_persona(self, user_id: uuid.UUID, persona_data: PersonaCreate) -> Persona:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        persona_count = self.db.query(Persona).filter(Persona.user_id == user_id).count()
        is_default = persona_count == 0
        
        persona = Persona(
            user_id=user_id,
            name=persona_data.name,
            persona_type=persona_data.persona_type,
            context=persona_data.context,
            professional_details=persona_data.professional_details or {},
            ai_settings=persona_data.ai_settings or {},
            is_default=is_default or persona_data.is_default
        )
        
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        
        if persona.is_default:
            user.default_persona_id = persona.id
            self.db.commit()
        
        return persona
    
    def create_default_persona(self, user_id: uuid.UUID) -> Persona:
        default_data = PersonaCreate(
            name="Professional",
            persona_type="professional",
            context={
                "profession": "Professional",
                "company": "",
                "communication_style": "professional"
            },
            professional_details={},
            is_default=True
        )
        return self.create_persona(user_id, default_data)
    
    def update_persona(self, user_id: uuid.UUID, persona_id: uuid.UUID, update_data: PersonaUpdate) -> Persona:
        persona = self.db.query(Persona).filter(
            and_(
                Persona.id == persona_id,
                Persona.user_id == user_id
            )
        ).first()
        
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        if update_data.is_default:
            self.db.query(Persona).filter(
                Persona.user_id == user_id,
                Persona.id != persona_id,
                Persona.is_default == True
            ).update({"is_default": False})
            
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                user.default_persona_id = persona_id
        
        for key, value in update_dict.items():
            setattr(persona, key, value)
        
        self.db.commit()
        self.db.refresh(persona)
        return persona
    
    def delete_persona(self, user_id: uuid.UUID, persona_id: uuid.UUID):
        persona = self.db.query(Persona).filter(
            and_(
                Persona.id == persona_id,
                Persona.user_id == user_id
            )
        ).first()
        
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        if persona.is_default:
            other_persona = self.db.query(Persona).filter(
                Persona.user_id == user_id,
                Persona.id != persona_id
            ).first()
            
            if other_persona:
                other_persona.is_default = True
                user = self.db.query(User).filter(User.id == user_id).first()
                if user:
                    user.default_persona_id = other_persona.id
        
        self.db.delete(persona)
        self.db.commit()
    
    def set_default_persona(self, user_id: uuid.UUID, persona_id: uuid.UUID):
        self.db.query(Persona).filter(
            Persona.user_id == user_id,
            Persona.is_default == True
        ).update({"is_default": False})
        
        persona = self.db.query(Persona).filter(
            Persona.id == persona_id,
            Persona.user_id == user_id
        ).first()
        
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        persona.is_default = True
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.default_persona_id = persona_id
        
        self.db.commit()

