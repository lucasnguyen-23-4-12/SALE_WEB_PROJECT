from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class OrderItemBase(BaseModel):
    order_id: str = Field(min_length=1, max_length=50)
    product_id: str = Field(min_length=1, max_length=50)
    quantity: int = Field(ge=1)
    amount: Optional[Decimal] = None
    price_at_purchase: Optional[Decimal] = None
    profit: Optional[Decimal] = None
    discount: Optional[Decimal] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    order_item_id: str

    model_config = {
        "from_attributes": True
    }
