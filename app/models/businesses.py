from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Float, ForeignKey, func
from typing import Optional
from datetime import datetime
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Business(Base):
    __tablename__ = 'business'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    business_name: Mapped[str] = mapped_column(String(255), index=True)
    city : Mapped[str] = mapped_column(String(255))
    category_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    latitude : Mapped[float] = mapped_column(Float, nullable=True)
    longitude : Mapped[float] = mapped_column(Float, nullable=True)
    gst_number : Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    gst_enabled : Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
