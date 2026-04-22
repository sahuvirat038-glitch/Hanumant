"""
7. routers/products.py

POST /products/create — create product (auth required)
GET /products — get all products for a business
GET /products/{id} — get single product
PATCH /products/{id} — update product (auth required)
PATCH /products/{id}/toggle — toggle active/inactive (auth required)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from app.auth.dependencies import get_current_user
from app.models.products import Product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/create", response_model=ProductResponse)
async def create(product: ProductCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.name == product.name))
    product_exist = result.scalar_one_or_none()

    if product_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

@router.get("/{id}", response_model=ProductResponse)
async def get_product(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()

    if product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product {product.name} not found"
        )
    return product

@router.patch("/{id}", response_model=ProductResponse)
async def update(id : UUID, product: ProductUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Product).where(Product.id == product.id))
    product_exist = result.scalar_one_or_none()

    if not product_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product {product.name} not exists"
        )

    product_data = product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product_exist, key, value)
    await db.commit()
    await db.refresh(product_exist)
    return product_exist


@router.patch("/{id}/toggle", response_model=ProductResponse)
async def toggle_category(id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail="Product does not exist"
        )
    product.is_active = not product.is_active
    await db.commit()
    await db.refresh(product)
    return product
