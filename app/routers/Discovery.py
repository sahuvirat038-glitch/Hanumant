from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.businesses import Business
from app.models.products import Product
from app.schemas.businesses import BusinessResponse
from app.schemas.products import ProductResponse

router = APIRouter(
    prefix="/discover",
    tags=["Discovery"]
)

@router.get("/businesses", response_model=List[BusinessResponse])
async def discover_businesses(
    name: Optional[str] = None,
    category_id: Optional[UUID] = None,
    city: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = select(Business).where(Business.is_verified == True)

    if name:
        query = query.where(Business.business_name.ilike(f"%{name}%"))

    if category_id:
        query = query.where(Business.category_id == category_id)

    if city:
        query = query.where(Business.city.ilike(f"%{city}%"))

    result = await db.execute(query)
    businesses = result.scalars().all()

    if not businesses:
        return []

    return businesses


@router.get("/products", response_model=List[ProductResponse])
async def discover_products(
    name: Optional[str] = None,
    category_id: Optional[UUID] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = select(Product).where(Product.is_active == True)

    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))

    if category_id:
        query = query.join(Business, Business.id == Product.business_id).where(Business.category_id == category_id)

    if min_price:
        query = query.where(Product.price >= min_price)

    if max_price:
        query = query.where(Product.price <= max_price)

    result = await db.execute(query)
    products = result.scalars().all()

    if not products:
        return []

    return products