from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.models.units import Category

class UnitsCreate(BaseModel):
    name: str
    symbol: str
    category: Category

class UnitUpdate(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    category: Optional[Category] = None

class UnitsResponse(BaseModel):
    id : UUID
    name : str
    symbol : str
    category : Category
    created_at : datetime

    class Config:
        from_attributes = True


