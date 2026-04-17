from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    stock_quantity: Decimal

class ProductResponse(BaseModel):
    id :UUID
    business_id : UUID
    unit_id: UUID
    name : str
    description : str
    price : Decimal
    stock_quantity : Decimal
    is_active : bool
    created : datetime
    updated_at : Optional[datetime]

    class Config:
        from_attributes = True
