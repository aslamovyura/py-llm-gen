from typing import Optional
from pydantic import EmailStr, Field
from .base import BaseEntity

class User(BaseEntity):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    hashed_password: str
    role: str = Field(..., pattern="^(admin|manager|user)$")
    phone_number: Optional[str] = Field(None, pattern="^\+?[1-9]\d{1,14}$")
    
    class Config:
        from_attributes = True 