from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Enum, func
from datetime import datetime
from enum import Enum as PyEnum
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Category(PyEnum):
    weight = "weight"
    volume = "volume"
    countable = "countable"
    length = "length"
    specialized = "specialized"

class Unit(Base):
    __tablename__ = 'units'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    symbol: Mapped[str] = mapped_column(String(255), unique=True)
    category: Mapped[Category] = mapped_column(Enum(Category))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
