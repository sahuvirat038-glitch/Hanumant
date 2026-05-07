from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.orders import Order, Status as OrderStatus
from app.models.retailers import Retailer
from app.services.notification_service import send_notification

scheduler = AsyncIOScheduler()

async def check_payment_reminders():
    async with AsyncSessionLocal() as db:
        # fetch all orders that are payment_pending for more than 3 days
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        result = await db.execute(
            select(Order).where(
                Order.status == OrderStatus.payment_pending,
                Order.delivered_at <= three_days_ago
            )
        )
        overdue_orders = result.scalars().all()

        for order in overdue_orders:
            # fetch retailer to get user_id
            ret_result = await db.execute(select(Retailer).where(Retailer.id == order.retailer_id))
            retailer = ret_result.scalar_one_or_none()
            if retailer:
                await send_notification(
                    retailer.user_id,
                    "Payment Reminder",
                    f"Your payment for order {order.id} is overdue. Please pay as soon as possible.",
                    db
                )

def start_scheduler():
    scheduler.add_job(check_payment_reminders, "interval", hours=24)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()