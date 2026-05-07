from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.models.analytics_events import AnalyticsEvents
from app.schemas.analytics_events import AnalyticsEventResponse, AnalyticsEventCreate
from app.models.businesses import Business
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.products import Product
from app.middleware.rate_limit import limiter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

@limiter.limit("30/minute")
@router.post("/log", response_model=AnalyticsEventResponse)
async def create_analytics_event(request: Request, analytics: AnalyticsEventCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    new_event = AnalyticsEvents(
        user_id = current_user.id,
        business_id = analytics.business_id,
        event_type = analytics.event_type,
        event_data = analytics.event_data,
    )
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

@router.get("/dashboard/{business_id}")
async def get_data(business_id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "business_owner":
        raise HTTPException(status_code=403, detail="Not a business owner")

    result = await db.execute(select(Business).where(Business.id == business_id, Business.user_id == current_user.id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Total orders
    total_orders_result = await db.execute(select(func.count(Order.id)).where(Order.business_id == business_id))
    total_orders = total_orders_result.scalar()

    # Total revenue
    total_revenue_result = await db.execute(select(func.sum(Order.total_amount)).where(Order.business_id == business_id, Order.status == "paid"))
    total_revenue = total_revenue_result.scalar() or 0

    # Top products
    top_products_result = await db.execute(
        select(Product.name, func.count(OrderItem.id).label("count"))
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .where(Order.business_id == business_id)
        .group_by(Product.name)
        .order_by(func.count(OrderItem.id).desc())
        .limit(5)
    )
    top_products = [{"name": row.name, "count": row.count} for row in top_products_result.all()]

    # Top retailers
    top_retailers_result = await db.execute(
        select(Order.retailer_id, func.count(Order.id).label("count"))
        .where(Order.business_id == business_id)
        .group_by(Order.retailer_id)
        .order_by(func.count(Order.id).desc())
        .limit(5)
    )
    top_retailers = [{"retailer_id": str(row.retailer_id), "count": row.count} for row in top_retailers_result.all()]

    # Recent events
    recent_events_result = await db.execute(
        select(AnalyticsEvents)
        .where(AnalyticsEvents.business_id == business_id)
        .order_by(AnalyticsEvents.created_at.desc())
        .limit(10)
    )
    recent_events = recent_events_result.scalars().all()

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "top_products": top_products,
        "top_retailers": top_retailers,
        "recent_events": recent_events,
    }
