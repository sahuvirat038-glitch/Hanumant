from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: Decimal
    stock_quantity: int
    unit_id: UUID

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    stock_quantity: Optional[int]
    unit_id: Optional[UUID]

class ProductResponse(BaseModel):
    id :UUID
    business_id : UUID
    unit_id: UUID
    name : str
    description : Optional[str]
    price : Decimal
    stock_quantity : int
    is_active : bool
    created_at : datetime
    updated_at : Optional[datetime]

    class Config:
        from_attributes = True
