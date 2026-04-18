from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class InvoiceResponse(BaseModel):
    id : UUID
    order_id : UUID
    subtotal: Decimal
    gst_amount: Decimal
    total: Decimal
    gst_enabled : bool
    pdf_path : Optional[str]
    invoice_number: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True