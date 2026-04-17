from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: float
    comment: Optional[str]

class ReviewResponse(BaseModel):
    id : UUID
    business_id : UUID
    retailer_id: UUID
    rating: float
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes =True
