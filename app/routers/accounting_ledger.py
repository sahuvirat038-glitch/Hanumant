from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.models.accounting_ledger import AccountLedger, EntryType
from app.schemas.accounting_ledger import AccountLedgerResponse
from app.models.businesses import Business

router = APIRouter(
    prefix="/ledger",
    tags=["Accounting_ledger"],
)

@router.get("/", response_model=List[AccountLedgerResponse])
async def get_ledger(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "business_owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not a business owner"
        )

    result = await db.execute(select(Business).where(Business.user_id == current_user.id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )

    result = await db.execute(select(AccountLedger).where(AccountLedger.business_id == business.id))
    ledger = result.scalars().all()
    return ledger

@router.get("/{retailer_id}", response_model=List[AccountLedgerResponse])
async def get_ledger_by_id(retailer_id: UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "business_owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not a business owner"
        )

    result = await db.execute(select(Business).where(Business.user_id == current_user.id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )

    result = await db.execute(select(AccountLedger).where(AccountLedger.business_id == business.id, AccountLedger.retailer_id == retailer_id))
    ledger = result.scalars().all()
    return ledger



