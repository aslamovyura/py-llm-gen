from datetime import datetime
from typing import Optional, List
from pydantic import Field
from .base import BaseEntity

class Request(BaseEntity):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    client_id: int
    equipment_category: str = Field(..., pattern="^(server|network|storage|other)$")
    required_specifications: dict = Field(default_factory=dict)
    quantity: int = Field(..., gt=0)
    priority: str = Field(..., pattern="^(low|medium|high)$")
    status: str = Field(..., pattern="^(draft|pending|approved|rejected|completed|cancelled)$")
    budget_min: Optional[float] = Field(None, ge=0)
    budget_max: Optional[float] = Field(None, ge=0)
    currency: str = Field(..., pattern="^(USD|EUR|GBP)$")
    desired_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True 