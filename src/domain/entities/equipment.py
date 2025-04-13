from typing import Optional, List
from pydantic import Field
from .base import BaseEntity

class Equipment(BaseEntity):
    name: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    manufacturer: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., pattern="^(server|network|storage|other)$")
    status: str = Field(..., pattern="^(available|in_use|maintenance|retired)$")
    purchase_date: Optional[datetime] = None
    warranty_end_date: Optional[datetime] = None
    location: Optional[str] = None
    specifications: dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True 