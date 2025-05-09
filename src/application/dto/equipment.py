from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class EquipmentCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    manufacturer: str = Field(..., min_length=1, max_length=100)
    category: str # Not using pattern here, will be validated by entity
    status: str # Not using pattern here, will be validated by entity
    purchase_date: Optional[datetime] = None
    warranty_end_date: Optional[datetime] = None
    location: Optional[str] = None
    specifications: Optional[Dict] = Field(default_factory=dict)
    tags: Optional[Dict] = Field(default_factory=dict)

class EquipmentUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=1, max_length=100)
    manufacturer: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = None
    status: Optional[str] = None
    purchase_date: Optional[datetime] = None
    warranty_end_date: Optional[datetime] = None
    location: Optional[str] = None
    specifications: Optional[Dict] = None
    tags: Optional[Dict] = None 