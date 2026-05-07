from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from typing import List
from uuid import UUID
from app.auth.dependencies import get_current_user

from app.models.conversations import Conversations
from app.schemas.conversations import ConversationResponse, ConversationCreate
from app.models.junction import Junction, Status
from app.models.businesses import Business
from app.models.retailers import Retailer

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

@router.post("/create", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(
        select(Conversations).where(
            Conversations.business_id == conversation.business_id,
            Conversations.retailer_id == conversation.retailer_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    result = await db.execute(
        select(Junction).where(
            Junction.business_id == conversation.business_id,
            Junction.retailer_id == conversation.retailer_id
        )
    )
    junction = result.scalar_one_or_none()

    is_connected = junction is not None and junction.status == Status.active

    new_conversation = Conversations(
        business_id=conversation.business_id,
        retailer_id=conversation.retailer_id,
        order_id=conversation.order_id,
        is_connected=is_connected,
        unconnected_message_count=0,
    )

    db.add(new_conversation)
    await db.commit()
    await db.refresh(new_conversation)
    return new_conversation

@router.get("/", response_model=List[ConversationResponse])
async def get_conversation(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role == "business_owner":
        result = await db.execute(select(Business).where(current_user.id == Business.user_id))
        business = result.scalar_one_or_none()
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )

        result = await db.execute(select(Conversations).where(Conversations.business_id == business.id))
        conversations = result.scalars().all()
        if not conversations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        return conversations

    elif current_user.role == "retailer":
        result = await db.execute(select(Retailer).where(current_user.id == Retailer.user_id))
        retailer = result.scalar_one_or_none()
        if not retailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Retailer not found"
            )

        result = await db.execute(select(Conversations).where(Conversations.retailer_id == retailer.id))
        conversations = result.scalars().all()
        if not conversations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        return conversations

"""
Steps to build:

Fetch the order by order_id
Fetch all order items where order_items.order_id == order_id
Calculate subtotal = sum of item.quantity * item.price_at_order
Generate invoice number = f"INV-{datetime.now().year}-{random 6 digit number}"
Create Invoices object with subtotal, total=subtotal (gst off by default), invoice_number, order_id
db.add(), await db.commit()

Now go build it and paste back.
"""





