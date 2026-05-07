from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timezone, datetime
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.schemas.messages import MessageCreate, MessageResponse
from app.models.messages import Messages, MessageType
from app.models.conversations import Conversations
from app.middleware.rate_limit import limiter

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@limiter.limit("30/minute")
@router.post("/create", response_model=MessageResponse)
async def create_message(request: Request, message: MessageCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Conversations).where(Conversations.id == message.conversation_id))
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversations not found"
        )

    if conversation.is_connected == False:
        if conversation.unconnected_message_count >= 10:
            raise HTTPException(
                status_code=403,
                detail="Message limit reached"
            )

        conversation.unconnected_message_count += 1

    new_message = Messages(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        content=message.content,
        message_type=MessageType.text,
    )
    conversation.last_message_at = datetime.now(timezone.utc)

    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message

@router.get("/{conversation_id}", response_model=List[MessageResponse])
async def get_message(conversation_id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Messages).where(Messages.conversation_id == conversation_id))
    message = result.scalars().all()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    return message


