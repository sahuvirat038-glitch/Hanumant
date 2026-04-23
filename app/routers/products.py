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
from app.database import get_db
from typing import List
from uuid import UUID

from app.models.businesses import Business
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from app.models.products import Product
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/create", response_model=ProductResponse)
async def create(product: ProductCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    biz_result = await db.execute(select(Business).where(Business.user_id == current_user.id))
    business = biz_result.scalar_one_or_none()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )

    result = await db.execute(select(Product).where(Product.name == product.name, Product.business_id == business.id))
    product_exist = result.scalar_one_or_none()
    if product_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )
    new_product = Product(
        business_id=business.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        unit_id=product.unit_id
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products


@router.get("/{id}", response_model=ProductResponse)
async def get_product_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.patch("/{id}", response_model=ProductResponse)
async def update(id: UUID, update_product: ProductUpdate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == id))
    product_exist = result.scalar_one_or_none()

    if not product_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product do not exist"
        )
    product_data = update_product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product_exist, key, value)
    await db.commit()
    await db.refresh(product_exist)
    return product_exist


@router.patch("/{id}/toggle", response_model=ProductResponse)
async def toggle_product(id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail="Product does not exist"
        )
    product.is_active = not product.is_active
    await db.commit()
    await db.refresh(product)
    return product
