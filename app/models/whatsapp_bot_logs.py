from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Enum, ForeignKey, func, JSON
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Status(str, PyEnum):
    processed = "processed"
    failed = "failed"
    pending = "pending"


class WhatsappBotLogs(Base):
    __tablename__ = 'whatsapp_bot_logs'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number: Mapped[str] = mapped_column(String(100), index=True)
    incoming_message: Mapped[str] = mapped_column(String, index=True)
    parsed_order : Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status : Mapped[Status] = mapped_column(Enum(Status), nullable=True)
    order_id : Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


