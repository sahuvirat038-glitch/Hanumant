from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.retailers import RetailerUpdate, RetailerCreate, RetailerResponse
from app.auth.dependencies import get_current_user
from app.models.retailers import Retailer
from uuid import UUID

router = APIRouter(
    prefix="/retailers",
    tags=["Retailers"],
)

@router.post("/create", response_model=RetailerResponse)
async def create_retailer(retailer: RetailerCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Retailer).where(Retailer.shop_name == retailer.shop_name)
    )
    retailer_exist = result.scalar_one_or_none()
    if retailer_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Retailer already exists"
        )
    new_retailer = Retailer(
        user_id=current_user.id,
        shop_name=retailer.shop_name,
        city=retailer.city
    )
    db.add(new_retailer)
    await db.commit()
    await db.refresh(new_retailer)
    return new_retailer

@router.get("/{id}", response_model=RetailerResponse)
async def get_retailer_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Retailer).where(Retailer.id == id))
    retailer = result.scalar_one_or_none()
    if not retailer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer not found"
        )
    return retailer

@router.patch("/{id}", response_model=RetailerResponse)
async def update_retailer(
    id: UUID,
    update_retailer: RetailerUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Retailer).where(Retailer.id == id))
    retailer_exist = result.scalar_one_or_none()
    if not retailer_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="retailer not found"
        )
    retailer_data = update_retailer.model_dump(exclude_unset=True)
    for key, value in retailer_data.items():
        setattr(retailer_exist, key, value)
    await db.commit()
    await db.refresh(retailer_exist)
    return retailer_exist



