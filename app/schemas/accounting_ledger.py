from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.models.accounting_ledger import EntryType


class AccountLedgerResponse(BaseModel):
    id : UUID
    business_id : UUID
    retailer_id : UUID
    order_id : UUID
    entry_type : EntryType
    debit : Decimal
    credit : Decimal
    running_balance : Decimal
    entry_date : datetime
    created_at : datetime

    class Config:
        from_attributes = True
