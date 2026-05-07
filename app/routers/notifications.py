from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.schemas.notifications import NotificationCreate, NotificationResponse
from app.models.notifications import Notifications, Type

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(current_user= Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Notifications).where(Notifications.user_id == current_user.id))
    notification = result.scalars().all()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return notification

@router.patch("/{id}/read", response_model=NotificationResponse)
async def read_notification(id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Notifications).where(Notifications.id == id))
    notification = result.scalar_one_or_none()
    notification.user_id == current_user.id
    if not notification:
        return []

    notification.is_read = True

    await db.commit()
    await db.refresh(notification)
    return notification
