from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from src.core.database import get_db
from src.core.security import Security
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = Security.decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_enterprise:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user

def get_persona_or_404(
    persona_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from src.models.persona import Persona
    import uuid
    
    try:
        persona_uuid = uuid.UUID(persona_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid persona ID")
    
    persona = db.query(Persona).filter(
        Persona.id == persona_uuid,
        Persona.user_id == current_user.id
    ).first()
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    return persona

