from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, func
from datetime import datetime
from typing import Optional
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Conversations(Base):
    __tablename__ = 'conversations'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("business.id"), nullable=False)
    retailer_id :  Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("retailer.id"), nullable=False)
    order_id : Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    is_connected : Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    unconnected_message_count : Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_message_at : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

