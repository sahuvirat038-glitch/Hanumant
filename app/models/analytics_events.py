from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, func, JSON
from datetime import datetime
from main.app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class AnalyticsEvents(Base):
    __tablename__ = 'analytics_events'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    business_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('business.id'), nullable=True)
    event_type : Mapped[str] = mapped_column(String, nullable=False)
    event_data : Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

