from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.auth.dependencies import get_current_user
from typing import List
from uuid import UUID
from sqlalchemy import func
from datetime import datetime

from app.schemas.payments import PaymentCreate, PaymentResponse
from app.models.payments import Payment, PaymentMode, Status as PaymentStatus
from app.models.orders import Order, Status as OrderStatus
from app.models.accounting_ledger import AccountLedger, EntryType

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    payment: PaymentCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "business_owner":
        raise HTTPException(status_code=403, detail="Not a business owner")

    result = await db.execute(select(Order).where(Order.id == payment.order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status not in [OrderStatus.payment_pending, OrderStatus.partially_paid, OrderStatus.delivered]:
        raise HTTPException(status_code=400, detail="Order is not ready for payment")

    new_payment = Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        payment_mode=payment.payment_mode,
        status=PaymentStatus.success,
        reference_number=payment.reference_number,
        payment_date=datetime.utcnow()
    )
    db.add(new_payment)
    await db.flush()
    await db.refresh(new_payment)

    total_paid_result = await db.execute(
        select(func.sum(Payment.amount)).where(
            Payment.order_id == payment.order_id,
            Payment.status == PaymentStatus.success
        )
    )
    total_paid = total_paid_result.scalar() or 0

    if total_paid >= order.total_amount:
        order.status = OrderStatus.paid
    else:
        order.status = OrderStatus.partially_paid

    # get previous running balance for this business/retailer
    balance_result = await db.execute(
        select(AccountLedger)
        .where(
            AccountLedger.business_id == order.business_id,
            AccountLedger.retailer_id == order.retailer_id
        )
        .order_by(AccountLedger.created_at.desc())
        .limit(1)
    )
    last_entry = balance_result.scalar_one_or_none()
    previous_balance = last_entry.running_balance if last_entry else 0

    new_ledger_entry = AccountLedger(
        business_id=order.business_id,
        retailer_id=order.retailer_id,
        order_id=order.id,
        entry_type=EntryType.payment,
        debit=0,
        credit=new_payment.amount,
        running_balance=previous_balance - new_payment.amount,
        entry_date=datetime.utcnow()
    )

    db.add(new_ledger_entry)
    await db.commit()
    await db.refresh(new_payment)
    return new_payment

@router.get("/{order_id}", response_model=List[PaymentResponse])
async def get_payment(order_id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Payment).where(Payment.order_id == order_id))
    order = result.scalars().all()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order
