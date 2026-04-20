from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.models.whatsapp_bot_logs import Status


class WhatsappBotLogCreate(BaseModel):
    phone_number : str

class WhatsappBotLogResponse(BaseModel):
    id : UUID
    phone_number : str
    incoming_message : str
    parsed_order : Optional[dict]
    status : Status
    order_id : Optional[UUID]
    created_at : datetime

    class Config:
        from_attributes = True
