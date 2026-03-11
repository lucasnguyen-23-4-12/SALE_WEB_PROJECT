from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class OrderItemInput(BaseModel):
    """Schema cho order item khi tạo order"""
    product_id: int = Field(ge=1)
    quantity: int = Field(ge=1)

class OrderBase(BaseModel):
    customer_id: int = Field(ge=1)
    payment_method_id: int = Field(ge=1)
    order_date: date
    status: str = Field(min_length=1, max_length=50)
    shipping_address: Optional[str] = None
    shipping_fee: Optional[float] = Field(default=0.0, ge=0)
    discount_amount: Optional[float] = Field(default=0.0, ge=0)

class OrderCreate(BaseModel):
    """Schema tạo order mới - client gửi items trong request"""
    customer_id: int = Field(ge=1)
    payment_method_id: int = Field(ge=1)
    items: List[OrderItemInput]

class OrderUpdate(BaseModel):
    status: Optional[str] = Field(default=None, min_length=1, max_length=50)

class OrderResponse(OrderBase):
    order_id: int

    model_config = {
        "from_attributes": True
    }
