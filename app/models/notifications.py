from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Enum, ForeignKey, func
from datetime import datetime
from enum import Enum as PyEnum
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Type(str, PyEnum):
    order_update = "order_update"
    payment = "payment"
    message = "message"
    system = "system"

class Notifications(Base):
    __tabelname__="notifications"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String)
    body : Mapped[str] = mapped_column(String)
    type : Mapped[Type] = mapped_column(Enum(Type), nullable=False)
    # reference_id (Optional UUID — points to order or message)
    is_read : Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now)



