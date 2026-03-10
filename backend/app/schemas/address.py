from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    customer_id: int
    street: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    zipcode: Optional[str] = None
    is_default: Optional[int] = 0

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    address_id: int

    model_config = {
        "from_attributes": True
    }