from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    task_id: Optional[int] = None

class ChatResponse(BaseModel):
    task_id: int
    final_answer: str

class ChatMessage(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
