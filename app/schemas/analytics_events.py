from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class AnalyticsEventResponse(BaseModel):
    id : UUID
    user_id : UUID
    business_id : Optional[UUID]
    event_type : str
    event_data : dict
    created_at : datetime

    class Config:
        from_attributes = True
