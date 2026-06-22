from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.core.config import settings
from src.core.database import engine, Base
from src.api.v1 import auth, users, personas, channels, messages, ai, onboarding

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown - Clean up if needed

app = FastAPI(
    title="UniInbox AI API",
    description="Personal AI Communication Agent",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(personas.router, prefix="/api/v1")
app.include_router(channels.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(onboarding.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to UniInbox AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "UniInbox AI"}

