from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.database import get_db
from src.core.security import Security
from src.models.user import User
from src.schemas.user import UserCreate, Token, UserResponse
from src.services.persona_service import PersonaService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed = Security.get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed,
        full_name=user_data.full_name,
        company=user_data.company,
        job_title=user_data.job_title
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create default persona
    persona_service = PersonaService(db)
    persona_service.create_default_persona(new_user.id)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not Security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = Security.create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    refresh_token = Security.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    try:
        payload = Security.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        
        access_token = Security.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
