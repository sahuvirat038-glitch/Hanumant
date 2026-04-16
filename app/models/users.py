from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Enum, func
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class AuthProvider(str, PyEnum):
    google = "google"
    email = "email"

class Role(str, PyEnum):
    super_admin = "super_admin"
    business_owner = "business_owner"
    retailer = "retailer"

class Users(Base):
    __tablename__ = 'users'

    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name : Mapped[str] = mapped_column(String(100), index=True)
    email : Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone : Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password : Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role : Mapped[Role] = mapped_column(Enum(Role), default=Role.retailer)
    provider : Mapped[AuthProvider] = mapped_column(Enum(AuthProvider), default=AuthProvider.email)
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified : Mapped[bool] = mapped_column(Boolean, default=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
