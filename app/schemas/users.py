from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from main.app.models.users import Role


class UsersCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: Role

class UsersLogin(BaseModel):
    email: str
    password: str

class UsersOutput(BaseModel):
    id : UUID
    name: str
    email: str
    phone: str
    role: Role
    is_active : bool
    is_verified : bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True




