from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class RequestCreateDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    client_id: int
    equipment_category: str # Assuming pattern validation like ^(server|network|storage|other)$ will be in the entity
    required_specifications: Dict = Field(default_factory=dict)
    quantity: int = Field(..., gt=0)
    priority: str # Assuming pattern validation like ^(low|medium|high)$ will be in the entity
    status: str # Assuming pattern validation like ^(draft|pending|approved|rejected|completed|cancelled)$ will be in the entity
    budget_min: Optional[float] = Field(None, ge=0)
    budget_max: Optional[float] = Field(None, ge=0)
    currency: str # Assuming pattern validation like ^(USD|EUR|GBP)$ will be in the entity
    desired_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True

class RequestUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    client_id: Optional[int] = None
    equipment_category: Optional[str] = None # Assuming pattern validation will be in the entity
    required_specifications: Optional[Dict] = None
    quantity: Optional[int] = Field(None, gt=0)
    priority: Optional[str] = None # Assuming pattern validation will be in the entity
    status: Optional[str] = None # Assuming pattern validation will be in the entity
    budget_min: Optional[float] = Field(None, ge=0)
    budget_max: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = None # Assuming pattern validation will be in the entity
    desired_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True 