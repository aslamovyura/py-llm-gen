from typing import Optional, List, Dict
from datetime import datetime
from pydantic import Field
from .base import BaseEntity

class Equipment(BaseEntity):
    name: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    manufacturer: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., pattern="^(medical|industrial|laboratory|office|safety|server|network|storage|other)$")
    status: str = Field(..., pattern="^(available|in_use|maintenance|retired|reserved)$")
    purchase_date: Optional[datetime] = None
    warranty_end_date: Optional[datetime] = None
    location: Optional[str] = None
    specifications: Dict = Field(default_factory=dict)
    tags: Dict = Field(default_factory=dict)
    
    class Config:
        from_attributes = True 