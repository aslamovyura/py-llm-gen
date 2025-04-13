from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .config import Base

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    phone_number = Column(String(20), nullable=True)

class Client(BaseModel):
    __tablename__ = "clients"
    
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    company_name = Column(String(100), nullable=True)
    contact_person = Column(String(100), nullable=True)
    notes = Column(String(1000), nullable=True)
    tags = Column(JSON, nullable=True)

class Equipment(BaseModel):
    __tablename__ = "equipment"
    
    name = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True, index=True, nullable=False)
    manufacturer = Column(String(100), nullable=False)
    category = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    purchase_date = Column(DateTime, nullable=True)
    warranty_end_date = Column(DateTime, nullable=True)
    location = Column(String(255), nullable=True)
    specifications = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)

class Request(BaseModel):
    __tablename__ = "requests"
    
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    equipment_category = Column(String(20), nullable=False)
    required_specifications = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    priority = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    currency = Column(String(3), nullable=False)
    desired_delivery_date = Column(DateTime, nullable=True)
    notes = Column(String(1000), nullable=True)
    tags = Column(JSON, nullable=True)
    
    client = relationship("Client", backref="requests")

class Offer(BaseModel):
    __tablename__ = "offers"
    
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    quantity = Column(Integer, nullable=False)
    delivery_date = Column(DateTime, nullable=True)
    warranty_period_months = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    terms_and_conditions = Column(String(2000), nullable=True)
    notes = Column(String(1000), nullable=True)
    additional_services = Column(JSON, nullable=True)
    discount_percentage = Column(Float, nullable=True)
    payment_terms = Column(String(20), nullable=False)
    custom_payment_terms = Column(String(255), nullable=True)
    
    request = relationship("Request", backref="offers")
    equipment = relationship("Equipment", backref="offers") 