from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

# Base
class CustomerBase(BaseModel):
    customer_name: str = Field(min_length=1, max_length=255)
    customer_email: EmailStr
    phone_number: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=500)

# Create
class CustomerCreate(CustomerBase):
    password: str = Field(min_length=6, max_length=128)

# Login
class CustomerLogin(BaseModel):
    email_or_phone: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)

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
