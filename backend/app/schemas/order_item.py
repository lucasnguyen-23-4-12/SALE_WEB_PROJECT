from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    amount: Optional[Decimal] = None
    price_at_purchase: Optional[Decimal] = None
    profit: Optional[Decimal] = None
    discount: Optional[Decimal] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    order_item_id: int

    model_config = {
        "from_attributes": True
    }