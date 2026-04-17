from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Json
from uuid import UUID
from typing import Optional


class AnalyticsEventResponse(BaseModel):
    id : UUID
    user_id : UUID
    business_id : UUID
    event_type : str
    event_data : Json
    created_at : datetime

    class Config:
        from_attributes = True
