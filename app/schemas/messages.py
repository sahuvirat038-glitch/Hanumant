from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from main.app.models.messages import MessageType

class MessageCreate(BaseModel):
    content : str

class MessageResponse(BaseModel):
    id : UUID
    conversation_id : UUID
    sender_id : UUID
    content : str
    message_type : MessageType
    is_read : bool
    created_at : datetime

    class Config:
        from_attributes = True

