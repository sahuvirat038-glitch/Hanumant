from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: UUID
    unit_id: UUID
    quantity : int
    order_id: UUID

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

"""

9. routers/order_items.py

POST /order-items/create — add item to order (auth required)
GET /order-items/{order_id} — get all items for an order (auth required)

"""