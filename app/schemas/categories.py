from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class CategoryCreate(BaseModel):
    name : str

class CategoryResponse(BaseModel):
    id : UUID
    name : str
    is_active : bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True