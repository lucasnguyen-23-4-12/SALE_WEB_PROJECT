from pydantic import BaseModel
from typing import Optional


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
