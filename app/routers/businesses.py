from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.businesses import BusinessCreate, BusinessResponse, BusinessUpdate
from app.auth.dependencies import get_current_user
from app.models.businesses import Business
from typing import List
from uuid import UUID

router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"]
)

@router.post("/create", response_model=BusinessResponse)
async def create_business(business: BusinessCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Business).where(Business.business_name == business.business_name)
    )
    business_exist = result.scalar_one_or_none()
    if business_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business already exists"
        )
    new_business = Business(
        user_id=current_user.id,
        business_name=business.business_name,
        city=business.city,
        category_id=business.category_id,
        gst_number=business.gst_number,
        gst_enabled=True if business.gst_number else False,
    )
    db.add(new_business)
    await db.commit()
    await db.refresh(new_business)
    return new_business


@router.get("/", response_model=List[BusinessResponse])
async def get_businesses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business))
    businesses = result.scalars().all()
    return businesses


@router.get("/{id}", response_model=BusinessResponse)
async def get_business_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business).where(Business.id == id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    return business


@router.patch("/{id}", response_model=BusinessResponse)
async def update_business(
    id: UUID,
    update_business: BusinessUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Business).where(Business.id == id))
    business_exist = result.scalar_one_or_none()
    if not business_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    business_data = update_business.model_dump(exclude_unset=True)
    for key, value in business_data.items():
        setattr(business_exist, key, value)
    await db.commit()
    await db.refresh(business_exist)
    return business_exist