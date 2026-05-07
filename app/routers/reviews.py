from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.models.reviews import Review
from app.schemas.reviews import ReviewCreate, ReviewResponse
from app.models.retailers import Retailer
from app.models.businesses import Business
from app.models.junction import Junction
from app.middleware.rate_limit import limiter

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)

@limiter.limit("10/minute")
@router.post("/create", response_model=ReviewResponse)
async def create_review(request: Request, reviews: ReviewCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "retailer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a retailer",
        )

    result = await db.execute(select(Retailer).where(Retailer.user_id == current_user.id))
    retailer = result.scalar_one_or_none()
    if not retailer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retailer not found",
        )

    biz_result = await db.execute(select(Business).where(Business.id == reviews.business_id))
    business = biz_result.scalar_one_or_none()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )

    existing_result = await db.execute(
        select(Junction).where(
            Junction.business_id == business.id,
            Junction.retailer_id == retailer.id
        )
    )
    junction_exist = existing_result.scalar_one_or_none()
    if not junction_exist or junction_exist.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Junction already exists or is not active"
        )

    result = await db.execute(select(Review).where(Review.business_id == business.id, Review.retailer_id == retailer.id))
    review_exist = result.scalar_one_or_none()
    if review_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review already exists"
        )

    new_review = Review(
        business_id=reviews.business_id,
        retailer_id=retailer.id,
        rating=reviews.rating,
        comment=reviews.comment,
    )

    result = await db.execute(select(Review).where(Review.business_id == reviews.business_id))
    all_reviews = result.scalars().all()
    ratings = [r.rating for r in all_reviews] + [reviews.rating]
    business.rating = sum(ratings) / len(ratings)

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

@router.get("/{business_id}", response_model=List[ReviewResponse])
async def get_review(business_id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Review).where(business_id == Review.business_id))
    review_business = result.scalars().all()
    if not review_business:
        return []

    return review_business