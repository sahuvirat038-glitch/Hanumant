from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Numeric, func
from datetime import datetime
from typing import Optional
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from decimal import Decimal


class Invoices(Base):
    __tablename__ = 'invoices'

    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    subtotal : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    gst_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    total : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    gst_enabled : Mapped[bool] = mapped_column(Boolean, default=False)
    pdf_path : Mapped[Optional[str]] = mapped_column(String)
    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now() , nullable=False)

