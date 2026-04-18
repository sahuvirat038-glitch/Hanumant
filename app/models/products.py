from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func, Numeric
from datetime import datetime
from typing import Optional
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from decimal import Decimal

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('business.id'), nullable=False)
    unit_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), index=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())




