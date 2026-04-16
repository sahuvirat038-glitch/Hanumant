from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from datetime import datetime
from typing import Optional
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    device_info : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ip_address : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_revoked : Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    expires_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
