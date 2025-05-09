from pydantic import BaseModel, Field, condecimal
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class OfferCreateDTO(BaseModel):
    request_id: int
    equipment_id: int
    price: condecimal(max_digits=12, decimal_places=2) = Field(..., ge=0)
    currency: str # Pattern validation will be handled by the entity
    quantity: int = Field(..., gt=0)
    delivery_date: Optional[datetime] = None
    warranty_period_months: int = Field(..., ge=0)
    status: str # Pattern validation will be handled by the entity
    terms_and_conditions: Optional[str] = None
    notes: Optional[str] = None
    additional_services: Optional[List[str]] = Field(default_factory=list)
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    payment_terms: str # Pattern validation will be handled by the entity
    custom_payment_terms: Optional[str] = None

class OfferUpdateDTO(BaseModel):
    request_id: Optional[int] = None
    equipment_id: Optional[int] = None
    price: Optional[condecimal(max_digits=12, decimal_places=2)] = Field(None, ge=0)
    currency: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    delivery_date: Optional[datetime] = None
    warranty_period_months: Optional[int] = Field(None, ge=0)
    status: Optional[str] = None
    terms_and_conditions: Optional[str] = None
    notes: Optional[str] = None
    additional_services: Optional[List[str]] = None
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    payment_terms: Optional[str] = None
    custom_payment_terms: Optional[str] = None 