from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class BusinessCreate(BaseModel):
    business_name: str
    city: str
    category_id: UUID
    gst_number: Optional[str] = None

class BusinessUpdate(BaseModel):
    business_name: Optional[str] = None
    city: Optional[str] = None
    category_id: Optional[UUID] = None
    gst_number: Optional[str] = None
    gst_enabled: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class BusinessResponse(BaseModel):
    id: UUID
    user_id: UUID
    business_name: str
    city: str
    category_id: UUID
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    gst_number: Optional[str] = None
    gst_enabled: Optional[bool] = None
    is_verified: bool
    rating: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True