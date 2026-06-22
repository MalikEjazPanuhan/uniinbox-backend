from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from src.core.config import settings
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Security:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @staticmethod
    def create_refresh_token(user_id: uuid.UUID) -> str:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {"sub": str(user_id), "exp": expire, "type": "refresh"}
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    
    @staticmethod
    def encrypt_data(data: str) -> str:
        cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        return cipher.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt_data(encrypted_data: str) -> str:
        cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        return cipher.decrypt(encrypted_data.encode()).decode()
    
    