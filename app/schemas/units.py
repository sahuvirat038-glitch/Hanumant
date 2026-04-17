from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from main.app.models.units import Category

class UnitsCreate(BaseModel):
    name: str
    symbol: str
    category: Category

class UnitsResponse(BaseModel):
    id : UUID
    name : str
    symbol : str
    category : Category
    created_at : datetime

    class Config:
        from_attributes = True


