from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.auth.dependencies import get_current_user
from typing import List
from uuid import UUID

from app.schemas.order_items import OrderItemCreate, OrderItemResponse
from app.models.order_items import OrderItem
from app.models.orders import Order, Status as OrderStatus
from app.models.products import Product
from app.models.retailers import Retailer

router = APIRouter(
    prefix="/order-items",
    tags=["Orders_Item"]
)

@router.post("/create", response_model=OrderItemResponse)
async def create_order_item(item: OrderItemCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "retailer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a retailer",
        )
    result = await db.execute(select(Retailer).where(Retailer.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    result = await db.execute(select(Order).where(Order.id == item.order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if not profile.id == order.retailer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order does not belong to retailer",
        )

    if not order.status == OrderStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is not pending",
        )

    result = await db.execute(select(Product).where(item.product_id == Product.id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if product.is_active == False or product.stock_quantity == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not active",
        )

    new_order = OrderItem(
        order_id=item.order_id,
        product_id=item.product_id,
        unit_id=item.unit_id,
        quantity=item.quantity,
        price_at_order=product.price
    )

    product.stock_quantity -= item.quantity
    order.total_amount += product.price * item.quantity
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/{id}", response_model=List[OrderItemResponse])
async def get_orders(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderItem).where(OrderItem.order_id == id))
    order = result.scalars().all()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order

