from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class OrderItemInput(BaseModel):
    """Schema cho order item khi tạo order"""
    product_id: int
    quantity: int

class OrderBase(BaseModel):
    customer_id: int
    payment_method_id: int
    order_date: date
    status: str

class OrderCreate(BaseModel):
    """Schema tạo order mới - client gửi items trong request"""
    customer_id: int
    payment_method_id: int
    items: List[OrderItemInput]

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderResponse(OrderBase):
    order_id: int

    model_config = {
        "from_attributes": True
    }