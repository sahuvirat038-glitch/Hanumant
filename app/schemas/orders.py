from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from main.app.models.orders import Status

class OrderCreate(BaseModel):
    business_id: UUID
    notes: Optional[str]

class OrderResponse(BaseModel):
    id: UUID
    business_id: UUID
    retailer_id: UUID
    status: Status
    total_amount: Decimal
    rejection_reason: Optional[str]
    notes: Optional[str]
    dispatched_at : Optional[datetime]
    delivered_at : Optional[datetime]
    confirmed_at : Optional[datetime]
    created_at : datetime
    updated_at : Optional[datetime]

    class Config:
        from_attributes = True