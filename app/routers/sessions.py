from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.schemas.sessions import SessionResponse
from app.models.sessions import Session

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

@router.get("/", response_model=List[SessionResponse])
async def get_sessions(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Session).where(Session.user_id == current_user.id, Session.is_revoked == False))
    sessions = result.scalars().all()
    if not sessions:
       return []

    return sessions

@router.delete("/{id}", response_model=SessionResponse)
async def get_sessions_by_id(id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Session).where(Session.id == id))
    sessions = result.scalar_one_or_none()
    if not sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sessions found"
        )

    if not sessions.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Session do not belong to current user"
        )

    sessions.is_revoked = True
    await db.commit()
    return sessions

