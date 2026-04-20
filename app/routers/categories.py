from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas.categories import CategoryCreate, CategoryResponse
from app.auth.dependencies import get_current_user
from app.models.categories import Category
from typing import List
from uuid import UUID


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.post("/create", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.name == category.name))
    category_exist = result.scalar_one_or_none()
    if category_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail="Category already exists"
        )
    new_category = Category(
        name=category.name
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

@router.get("/get_category", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.is_active == True))
    categories = result.scalars().all()
    return categories

@router.patch("/{id}", response_model=CategoryResponse)
async def toggle_category(id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail="Category does not exist"
        )
    category.is_active = not category.is_active
    await db.commit()
    await db.refresh(category)
    return category