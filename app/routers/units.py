from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.units import UnitsCreate, UnitsResponse, UnitUpdate
from app.auth.dependencies import get_current_user
from app.models.units import Unit
from typing import List
from uuid import UUID


router = APIRouter(
    prefix="/units",
    tags=["Units"],
)

@router.post("/create", response_model=UnitsResponse)
async def create_units(units: UnitsCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).where(Unit.name == units.name))
    units_exist = result.scalar_one_or_none()
    if units_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail="Unit already exists"
        )
    new_unit = Unit(
        name=units.name,
        symbol=units.symbol,
        category=units.category,
    )
    db.add(new_unit)
    await db.commit()
    await db.refresh(new_unit)
    return new_unit


@router.get("/get_units", response_model=List[UnitsResponse])
async def get_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit))
    units = result.scalars().all()
    return units

@router.patch("/{id}", response_model=UnitsResponse)
async def update_units(id: UUID, update_unit: UnitUpdate, current_user=Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).where(Unit.id == id))
    unit_exist = result.scalar_one_or_none()

    if not unit_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail="Unit does not exist"
        )

    unit_data = update_unit.model_dump(exclude_unset=True)
    for key, value in unit_data.items():
        setattr(unit_exist, key, value)
    await db.commit()
    await db.refresh(unit_exist)
    return unit_exist
