from datetime import datetime
from random import randint
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.invoices import Invoices
from app.utils.pdf_generator import generate_invoice_pdf


async def generate_invoices(order_id: UUID, db: AsyncSession):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise Exception(f"Order {order_id} not found")

    result = await db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
    order_items = result.scalars().all()
    if not order_items:
        raise Exception(f"Order Item not found")

    subtotal = sum(item.quantity * item.price_at_order for item in order_items)
    invoice_number = f"INV-{datetime.now().year}-{randint(100000, 999999)}"
    new_invoice = Invoices(
        order_id=order.id,
        subtotal=subtotal,
        gst_amount=0,
        total=subtotal,
        invoice_number=invoice_number,
        gst_enabled=False,
    )

    db.add(new_invoice)
    await db.commit()
    await db.refresh(new_invoice)
    pdf_path = generate_invoice_pdf(new_invoice)
    new_invoice.pdf_path = pdf_path
    await db.commit()
    return new_invoice