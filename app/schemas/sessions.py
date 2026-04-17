from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class SessionResponse(BaseModel):
    id : UUID
    user_id : UUID
    token : str
    device_info : Optional[str]
    ip_address : Optional[str]
    expires_at : datetime
    created_at : datetime

    class Config:
        from_attributes = True


