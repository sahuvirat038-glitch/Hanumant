from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Enum, ForeignKey, func, Numeric
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from decimal import Decimal

class Status(str, PyEnum):
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"
    dispatched = "dispatched"
    delivered = "delivered"
    payment_pending = "payment_pending"
    partially_paid = "partially_paid"
    paid = "paid"

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("business.id"))
    retailer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("retailer.id"))
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.pending)
    total_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    rejection_reason : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dispatched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())



