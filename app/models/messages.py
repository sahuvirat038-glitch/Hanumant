from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Enum, ForeignKey, func
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class MessageType(str, PyEnum):
    text = "text"
    image = "image"

class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    sender_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    content : Mapped[str] = mapped_column(String, nullable=False)
    message_type : Mapped[MessageType] = mapped_column(Enum(MessageType), nullable=False)
    is_read : Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

