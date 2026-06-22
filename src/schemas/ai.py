from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID

class AISuggestionRequest(BaseModel):
    message_id: UUID
    persona_id: UUID
    context: Optional[Dict[str, Any]] = None
    num_suggestions: int = 3

class AISuggestionResponse(BaseModel):
    suggestions: List[Dict[str, Any]]
    persona_name: str
    model_used: str

class AIDraftRequest(BaseModel):
    persona_id: UUID
    purpose: str
    recipient: str
    key_points: List[str] = []
    context: Optional[str] = None
    tone: str = "professional"
    length: str = "medium"

class AIDraftResponse(BaseModel):
    draft: str
    persona_name: str
    model_used: str

class AISummarizeRequest(BaseModel):
    thread_id: UUID
    persona_id: UUID
    max_length: Optional[int] = 500

class AISummarizeResponse(BaseModel):
    summary: str
    key_points: List[str]
    action_items: List[str]

