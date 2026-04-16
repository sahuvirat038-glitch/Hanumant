from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from datetime import datetime
from typing import Optional
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Review(Base):
    __tablename__ = "reviews"

    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    business_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("business.id"), nullable=False)
    retailer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("retailer.id"), nullable=False)
    rating : Mapped[int] = mapped_column(Integer, default=0, nullable=False)# range 1 to 5
    comment : Mapped[Optional[str]] = mapped_column(String, null=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())



