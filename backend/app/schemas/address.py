from pydantic import BaseModel, Field
from typing import Optional

class AddressBase(BaseModel):
    customer_id: str = Field(min_length=1, max_length=50)
    street: Optional[str] = Field(default=None, max_length=500)
    city: Optional[str] = Field(default=None, max_length=100)
    district: Optional[str] = Field(default=None, max_length=100)
    zipcode: Optional[str] = Field(default=None, max_length=20)
    is_default: int = Field(default=0, ge=0, le=1)

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    address_id: str

    model_config = {
        "from_attributes": True
    }
