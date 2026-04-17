from pydantic import BaseModel, Json
from uuid import UUID
from typing import Optional
from datetime import datetime
from main.app.models.whatsapp_bot_logs import Status


class WhatsappBotLogCreate(BaseModel):
    phone_number : str

class WhatsappBotLogResponse(BaseModel):
    id : UUID
    phone_number : str
    incoming_message : str
    parsed_order : Json
    status : Status
    order_id : UUID
    created_at : datetime

    class Config:
        from_attributes = True