from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.models.notifications import Type

class NotificationCreate(BaseModel):
    title: str
    body: str
    type: Type
    reference_id: Optional[UUID]

class NotificationResponse(BaseModel):
    id : UUID
    user_id: UUID
    title: str
    body: str
    type: Type
    reference_id: Optional[UUID]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
