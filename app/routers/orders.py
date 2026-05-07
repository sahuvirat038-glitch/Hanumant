"""
8. routers/orders.py

POST /orders/create — retailer places order (auth required)
GET /orders — get all orders (auth required)
GET /orders/{id} — get single order (auth required)
PATCH /orders/{id}/confirm — business owner confirms (auth required)
PATCH /orders/{id}/reject — business owner rejects (auth required)
PATCH /orders/{id}/dispatch — business owner dispatches (auth required)
PATCH /orders/{id}/deliver — mark as delivered (auth required)

"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user
from datetime import datetime, timezone

from app.services.invoice_service import generate_invoices
from app.schemas.orders import OrderCreate, OrderResponse, OrderReject
from app.models.orders import Order, Status as OrderStatus
from app.models.junction import Junction, Status as JunctionStatus
from app.models.businesses import Business
from app.models.retailers import Retailer
from app.models.users import Users, Role as UserRole
from app.services.notification_service import send_notification
from app.middleware.rate_limit import limiter



router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@limiter.limit("20/minute")
@router.post("/create", response_model=OrderResponse)
async def create(request: Request, order: OrderCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.retailer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a retailer"
        )
    result = await db.execute(select(Retailer).where(Retailer.user_id == current_user.id))
    retailer_profile = result.scalar_one_or_none()

    if not retailer_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer not found"
        )
    result = await db.execute(select(Junction).where(Junction.retailer_id == retailer_profile.id, Junction.status == JunctionStatus.active))
    junction_exist = result.scalar_one_or_none()

    if not junction_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Junction not found"
        )
    new_order = Order(
        business_id=order.business_id,
        retailer_id=retailer_profile.id,
        status=OrderStatus.pending,
        total_amount=0,
        notes=order.notes,
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


@router.get("/", response_model=List[OrderResponse])
async def get_order(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role == "business_owner":
        bus_result = await db.execute(select(Business).where(Business.user_id == current_user.id))
        business = bus_result.scalar_one_or_none()

        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )

        result = await db.execute(select(Order).where(Order.business_id == business.id))
        orders = result.scalars().all()
        return orders

    elif current_user.role == "retailer":
        ret_result = await db.execute(
            select(Retailer).where(Retailer.user_id == current_user.id)
        )
        retailer = ret_result.scalar_one_or_none()

        if not retailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Retailer profile not found"
            )

        result = await db.execute(select(Order).where(Order.retailer_id == retailer.id))
        order = result.scalars().all()
        return order
    else:
        return []

@router.get("/{id}", response_model=OrderResponse)
async def get_by_id(id: UUID, current_user= Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == id))
    order_exist = result.scalar_one_or_none()

    if not order_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order dont exist"
        )
    return order_exist

@router.patch("/{id}/confirm", response_model=OrderResponse)
async def confirm(id: UUID, current_user= Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != "business_owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a business owner"
        )

    result = await db.execute(select(Order).where(Order.id == id))
    order_exist = result.scalar_one_or_none()
    if not order_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    is_pending = order_exist.status == OrderStatus.pending
    if not is_pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order not pending"
        )

    order_exist.status = OrderStatus.confirmed
    order_exist.confirmed_at = datetime.now(timezone.utc)
    # fetch retailer to get user_id
    ret_result = await db.execute(select(Retailer).where(Retailer.id == order_exist.retailer_id))
    retailer = ret_result.scalar_one_or_none()

    await send_notification(retailer.user_id, "Order Confirmed", "Your order has been confirmed", db)
    await generate_invoices(order_exist.id, db)
    await db.commit()
    await db.refresh(order_exist)
    return order_exist

@router.patch("/{id}/reject", response_model=OrderResponse)
async def reject(id: UUID, data: OrderReject, current_user= Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    if current_user.role != "business_owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a business owner"
        )

    result = await db.execute(select(Order).where(Order.id == id))
    order_exist = result.scalar_one_or_none()
    if not order_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    is_pending = order_exist.status == OrderStatus.pending
    if not is_pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order not pending"
        )

    order_exist.status = OrderStatus.rejected
    order_exist.rejection_reason = data.rejection_reason
    # fetch retailer to get user_id
    ret_result = await db.execute(select(Retailer).where(Retailer.id == order_exist.retailer_id))
    retailer = ret_result.scalar_one_or_none()

    await send_notification(retailer.user_id, "Order Rejected", "Your order has been rejected", db)
    await db.commit()
    await db.refresh(order_exist)
    return order_exist


@router.patch("/{id}/dispatch", response_model=OrderResponse)
async def dispatch(id: UUID, current_user= Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != "business_owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a business owner"
        )

    result = await db.execute(select(Order).where(Order.id == id))
    order_exist = result.scalar_one_or_none()
    if not order_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    is_confirmed = order_exist.status == OrderStatus.confirmed
    if not is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order not confirmed"
        )

    order_exist.status = OrderStatus.dispatched
    order_exist.dispatched_at = datetime.now(timezone.utc)
    # fetch retailer to get user_id
    ret_result = await db.execute(select(Retailer).where(Retailer.id == order_exist.retailer_id))
    retailer = ret_result.scalar_one_or_none()

    await send_notification(retailer.user_id, "Order Dispatch", "Your order has been dispatch", db)
    await db.commit()
    await db.refresh(order_exist)
    return order_exist

@router.patch("/{id}/deliver", response_model=OrderResponse)
async def deliver(id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Order).where(Order.id == id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    is_dispatched = order.status == OrderStatus.dispatched
    if not is_dispatched:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not a dispatched order"
        )

    order.status = OrderStatus.delivered
    order.delivered_at = datetime.now(timezone.utc)
    await db.commit()
    # fetch retailer to get user_id
    ret_result = await db.execute(select(Retailer).where(Retailer.id == order.retailer_id))
    retailer = ret_result.scalar_one_or_none()

    await send_notification(retailer.user_id, "Order Delivered", "Your order has been delivered", db)
    order.status = OrderStatus.payment_pending
    await db.commit()
    await db.refresh(order)
    return order



