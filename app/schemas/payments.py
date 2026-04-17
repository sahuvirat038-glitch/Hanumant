from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from main.app.models.payments import PaymentMode, Status


class PaymentCreate(BaseModel):
    amount: Decimal
    payment_mode: PaymentMode
    status: Status

class PaymentResponse(BaseModel):
    id : UUID
    order_id : UUID
    amount : Decimal
    payment_mode : PaymentMode
    status : Status
    reference_number : Optional[str]
    payment_date : datetime
    created_at: datetime

    class Config:
        from_attributes = True
