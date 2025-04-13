from typing import Optional, List
from pydantic import EmailStr, Field
from .base import BaseEntity

class Client(BaseEntity):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: Optional[str] = Field(None, pattern="^\+?[1-9]\d{1,14}$")
    address: Optional[str] = None
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True 