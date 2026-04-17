from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class ConversationResponse(BaseModel):
    id : UUID
    business_id : UUID
    retailer_id : UUID
    order_id : Optional[UUID]
    is_connected : bool
    unconnected_message_count : int
    last_message_at : Optional[datetime]
    created_at : datetime

    class Config:
        from_attributes = True

