from uuid import UUID
from app.models.notifications import Notifications, Type

async def send_notification(user_id: UUID, title: str, body: str, db):
    notification = Notifications(
        user_id=user_id,
        title=title,
        body=body,
        type=Type.order_update
    )
    db.add(notification)
    await db.commit()