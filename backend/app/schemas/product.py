from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    product_name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    unit_price: Decimal
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    unit_price: Optional[Decimal] = None
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    product_id: int

    model_config = {
        "from_attributes": True
    }