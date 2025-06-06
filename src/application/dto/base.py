from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BaseDTO(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 