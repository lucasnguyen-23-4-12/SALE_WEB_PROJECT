from pydantic import BaseModel
from typing import Optional
from datetime import date

class OrderBase(BaseModel):
    customer_id: int
    payment_method_id: int
    order_date: date
    status: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderResponse(OrderBase):
    order_id: int

    model_config = {
        "from_attributes": True
    }