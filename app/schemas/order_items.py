from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: UUID
    unit_id: UUID
    quantity : int

class OrderItemResponse(BaseModel):
    id : UUID
    order_id : UUID
    product_id : UUID
    unit_id : UUID
    quantity : int
    price_at_order : Decimal
    created_at : datetime

    class Config:
        from_attributes = True
