"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.junction import Junction, Status
from app.models.businesses import Business
from app.models.users import Users, Role
from app.models.retailers import Retailer
from app.schemas.junction import JunctionResponse, JunctionCreate
from typing import List
from uuid import UUID

router = APIRouter(
    prefix="/junction",
    tags=["Junction"]
)

@router.post("/invite", response_model=JunctionResponse)
async def invite(
    junction: JunctionCreate,
    current_user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "business_owner":
        raise HTTPException(status_code=403, detail="Not a business owner")

    biz_result = await db.execute(select(Business).where(Business.user_id == current_user.id))
    business = biz_result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    retailer_result = await db.execute(select(Retailer).where(Retailer.id == junction.retailer_id))
    retailer = retailer_result.scalar_one_or_none()
    if not retailer or Retailer.role != Role.retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")

    existing_result = await db.execute(
        select(Junction).where(
            Junction.business_id == business.id,
            Junction.retailer_id == junction.retailer_id
        )
    )
    existing_junction = existing_result.scalar_one_or_none()
    if existing_junction:
        raise HTTPException(status_code=400, detail=f"Relationship already exists with status: {existing_junction.status}")

    new_junction = Junction(
        business_id=business.id,
        retailer_id=junction.retailer_id,
        status=Status.pending
    )
    db.add(new_junction)
    await db.commit()
    await db.refresh(new_junction)
    return new_junction


@router.patch("/{id}/accept", response_model=JunctionResponse)
async def accept(
    id: UUID,
    current_user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "retailer":
        raise HTTPException(status_code=403, detail="Not a retailer")

    result = await db.execute(select(Junction).where(Junction.id == id))
    junction = result.scalar_one_or_none()
    if not junction:
        raise HTTPException(status_code=404, detail="Junction not found")

    if junction.status != Status.pending:
        raise HTTPException(status_code=400, detail="Junction is not pending")

    junction.status = Status.active
    await db.commit()
    await db.refresh(junction)
    return junction


@router.patch("/{id}/block", response_model=JunctionResponse)
async def block(
    id: UUID,
    current_user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "business_owner":
        raise HTTPException(status_code=403, detail="Not a business owner")

    result = await db.execute(select(Junction).where(Junction.id == id))
    junction = result.scalar_one_or_none()
    if not junction:
        raise HTTPException(status_code=404, detail="Junction not found")

    junction.status = Status.blocked
    await db.commit()
    await db.refresh(junction)
    return junction


@router.get("/my-retailers", response_model=List[JunctionResponse])
async def my_retailers(
    current_user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "business_owner":
        raise HTTPException(status_code=403, detail="Not a business owner")

    biz_result = await db.execute(select(Business).where(Business.user_id == current_user.id))
    business = biz_result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    result = await db.execute(
        select(Junction).where(
            Junction.business_id == business.id,
            Junction.status == Status.active
        )
    )
    junctions = result.scalars().all()
    return junctions
"""