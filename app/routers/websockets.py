from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.websockets.manager import manager
from app.models.messages import Messages, MessageType
from app.models.conversations import Conversations
import json

router = APIRouter(
    tags=["Websockets"]
)

@router.websocket("/ws/{conversation_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    # verify conversation exists
    result = await db.execute(select(Conversations).where(Conversations.id == UUID(conversation_id)))
    conversation = result.scalar_one_or_none()
    if not conversation:
        await websocket.close(code=4004)
        return

    await manager.connect(conversation_id, websocket)

    try:
        while True:
            # wait for message from client
            data = await websocket.receive_text()

            # save message to DB
            new_message = Messages(
                conversation_id=UUID(conversation_id),
                sender_id=UUID(user_id),
                content=data,
                message_type=MessageType.text,
            )
            conversation.last_message_at = datetime.utcnow()
            db.add(new_message)
            await db.commit()
            await db.refresh(new_message)

            # broadcast to everyone in the conversation
            payload = json.dumps({
                "id": str(new_message.id),
                "conversation_id": conversation_id,
                "sender_id": user_id,
                "content": data,
                "created_at": str(new_message.created_at)
            })
            await manager.broadcast(conversation_id, payload)

    except WebSocketDisconnect:
        manager.disconnect(conversation_id, websocket)