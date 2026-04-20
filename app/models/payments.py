from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Enum, ForeignKey, func, Numeric
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from decimal import Decimal

class PaymentMode(str, PyEnum):
    offline = "offline"
    online = "online"
    cash = "cash"

class Status(str, PyEnum):
    success = "success"
    failed = "failed"
    pending = "pending"

class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    payment_mode: Mapped[PaymentMode] = mapped_column(Enum(PaymentMode), nullable=False, default=PaymentMode.offline)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default=Status.pending)
    reference_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
