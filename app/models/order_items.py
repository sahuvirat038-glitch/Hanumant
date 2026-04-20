from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, ForeignKey, func, Numeric
from datetime import datetime
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from decimal import Decimal


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    unit_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("units.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_order:Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


