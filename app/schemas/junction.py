from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.models.junction import Status

class JunctionCreate(BaseModel):
    retailer_id: UUID

class JunctionResponse(BaseModel):
    id: UUID
    business_id: UUID
    retailer_id: UUID
    status: Status
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True