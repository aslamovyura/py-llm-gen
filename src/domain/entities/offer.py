from datetime import datetime
from typing import Optional, List
from pydantic import Field, condecimal
from decimal import Decimal
from .base import BaseEntity

class Offer(BaseEntity):
    request_id: int
    equipment_id: int
    price: condecimal(max_digits=12, decimal_places=2) = Field(..., ge=0)
    currency: str = Field(..., pattern="^(USD|EUR|GBP)$")
    quantity: int = Field(..., gt=0)
    delivery_date: Optional[datetime] = None
    warranty_period_months: int = Field(..., ge=0)
    status: str = Field(..., pattern="^(draft|pending|accepted|rejected|cancelled)$")
    terms_and_conditions: Optional[str] = None
    notes: Optional[str] = None
    additional_services: List[str] = Field(default_factory=list)
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    payment_terms: str = Field(..., pattern="^(immediate|30_days|60_days|90_days|custom)$")
    custom_payment_terms: Optional[str] = None
    
    class Config:
        from_attributes = True 