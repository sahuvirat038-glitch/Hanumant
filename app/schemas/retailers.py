from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class RetailerCreate(BaseModel):
    shop_name : str
    city : str

class RetailerResponse(BaseModel):
    id : UUID
    user_id : UUID
    shop_name : str
    latitude : float
    longitude : float
    city : str
    created_at : datetime
    updated_at : Optional[datetime]

    class Config:
        from_attributes = True

