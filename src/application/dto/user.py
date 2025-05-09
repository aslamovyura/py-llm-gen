from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: str # Should be handled securely, this is just for DTO structure
    role: str # Consider using an Enum or specific validation
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdateDTO(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    # Not including hashed_password in update typically, or it's a separate flow
    role: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None # Common field in user updates

    class Config:
        from_attributes = True 