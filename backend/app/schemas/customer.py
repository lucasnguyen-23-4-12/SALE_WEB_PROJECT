from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Base
class CustomerBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None

# Create
class CustomerCreate(CustomerBase):
    password: str

# Login
class CustomerLogin(BaseModel):
    email_or_phone: str
    password: str

# Update
class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

# Response
class CustomerResponse(CustomerBase):
    customer_id: int
    created_at: Optional[date]
    updated_at: Optional[date]
    is_active: Optional[int]

    model_config = {
        "from_attributes": True
    }