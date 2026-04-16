from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Enum, ForeignKey, func, Numeric
from datetime import datetime
from enum import Enum as PyEnum
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class EntryType(str, PyEnum):
    sale = "sale"
    payment = "payment"
    adjustment = "adjustment"


class AccountLedger(Base):
    __tablename__ = 'accounting_ledger'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('business.id'), nullable=False)
    retailer_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('retailer.id'), nullable=False)
    order_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('order.id'), nullable=False)
    entry_type : Mapped[EntryType] = mapped_column(Enum(EntryType), nullable=False)
    debit : Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    credit : Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    running_balance : Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    entry_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

