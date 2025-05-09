from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

class ClientCreateDTO(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = []

class ClientUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None 