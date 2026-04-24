"""
6. routers/junction.py

POST /junction/invite — business owner invites retailer (auth required)
PATCH /junction/{id}/accept — retailer accepts invite (auth required)
PATCH /junction/{id}/block — business owner blocks retailer (auth required)
GET /junction/my-retailers — business owner gets all their retailers (auth required)

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.models.junction import Junction, Status
from app.models.users import Users
from app.schemas.junction import JunctionCreate, JunctionResponse
from app.models.businesses import Business
from app.models.retailers import Retailer

router = APIRouter(
    prefix="/junction",
    tags=["Junction"],
)

@router.post("/invite", response_model=JunctionResponse)
async def invite(junction: JunctionCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "business_owner":
        raise HTTPException(status_code=403, detail="Not a business owner")

    biz_result = await db.execute(select(Business).where(Business.user_id == current_user.id))
    business = biz_result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    retailer_result = await db.execute(select(Retailer).where(Retailer.id == junction.retailer_id))
    retailer_exist = retailer_result.scalar_one_or_none()
    if not retailer_exist:
        raise HTTPException(status_code=404, detail="Retailer not found")

    existing_result = await db.execute(
        select(Junction).where(
            Junction.business_id == business.id,
            Junction.retailer_id == junction.retailer_id
        )
    )
    junction_exist = existing_result.scalar_one_or_none()
    if junction_exist:
        raise HTTPException(status_code=400, detail="Junction already exists")

    new_junction = Junction(
        business_id=business.id,
        retailer_id=junction.retailer_id,
        status=Status.pending,
    )
    db.add(new_junction)  
    await db.commit()
    await db.refresh(new_junction)
    return new_junction




