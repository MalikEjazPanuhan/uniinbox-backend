from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # App
    APP_NAME: str = "UniInbox AI"
    DEBUG: bool = False
    SECRET_KEY: str
    ENCRYPTION_KEY: str
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    
    # Redis
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # AI
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEFAULT_LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4-turbo-preview"
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Gmail
    GMAIL_CLIENT_ID: Optional[str] = None
    GMAIL_CLIENT_SECRET: Optional[str] = None
    GMAIL_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/gmail/callback"
    
    # Slack
    SLACK_CLIENT_ID: Optional[str] = None
    SLACK_CLIENT_SECRET: Optional[str] = None
    SLACK_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/slack/callback"

settings = Settings()

