from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class BusinessCreate(BaseModel):
    business_name: str
    city : str
    category_id :UUID
    gst_number : Optional[str]

class BusinessResponse(BaseModel):
    id : UUID
    user_id : UUID
    business_name: str
    city: str
    category_id: UUID
    latitude : float
    longitude: float
    gst_number: Optional[str]
    gst_enabled : bool
    is_verified : bool
    rating : float
    created_at : datetime
    updated_at : Optional[datetime]

    class Config:
        from_attributes = True


