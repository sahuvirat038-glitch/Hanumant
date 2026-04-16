from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Enum, ForeignKey, func
from datetime import datetime
from enum import Enum as PyEnum
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Status(str, PyEnum):
    pending = "pending"
    active = "active"
    blocked = "blocked"

class Junction(Base):
    __tablename__ = 'junctions'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('business.id'), nullable=False)
    retailer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('retailer.id'), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())





