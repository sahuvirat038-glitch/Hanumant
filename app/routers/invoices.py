from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from uuid import UUID

from app.models.invoices import Invoices
from app.schemas.invoices import InvoiceResponse

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

@router.get("/{order_id}", response_model=InvoiceResponse)
async def get_invoice(order_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invoices).where(Invoices.order_id == order_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    return invoice