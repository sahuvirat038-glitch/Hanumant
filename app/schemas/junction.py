from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.models.junction import Status

class JunctionResponse(BaseModel):
    id : UUID
    business_id : UUID
    retailer_id : UUID
    status : Status
    created_at : datetime
    updated_at : Optional[datetime]

    class Config:
        from_attributes = True
