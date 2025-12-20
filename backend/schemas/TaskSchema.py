from pydantic import BaseModel
from datetime import datetime
from typing import List
from schemas.ChatSchema import ChatMessage

class TaskResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskDetailResponse(TaskResponse):
    chats: List[ChatMessage] = []
