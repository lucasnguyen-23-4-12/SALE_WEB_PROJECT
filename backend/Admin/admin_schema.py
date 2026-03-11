from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    description: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    description: Optional[str] = None


class ProductResponse(BaseModel):
    name: str
    price: float
    stock: int
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: date | datetime | None = None

    model_config = {
        "from_attributes": True
    }


class OrderStatusUpdate(BaseModel):
    status: Literal["pending", "processing", "shipped", "delivered", "cancelled"]
