from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.order import OrderResponse
from app.schemas.product import ProductCreate, ProductUpdate


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str


class AdminDashboardStats(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    total_categories: int
    pending_orders: int
    low_stock_products: int
    active_discount_codes: int
    total_revenue: Decimal


class AdminProductResponse(BaseModel):
    product_id: str
    category_id: str
    category_name: Optional[str] = None
    product_name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    unit_price: Decimal
    discount_percent: int
    stock_quantity: int
    rating_avg: Decimal
    total_reviews: int
    sold_quantity: int = 0


class AdminOrderResponse(OrderResponse):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None


class AdminDashboardResponse(BaseModel):
    stats: AdminDashboardStats
    recent_orders: list[AdminOrderResponse]
    top_products: list[AdminProductResponse]
    low_stock_products: list[AdminProductResponse]


class AdminCustomerResponse(BaseModel):
    customer_id: str
    customer_name: str
    customer_email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    is_active: bool = True
    orders_count: int = 0
    total_spent: Decimal = Decimal("0")
    last_order_date: Optional[date] = None


class AdminCustomerUpdate(BaseModel):
    customer_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    customer_email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=500)
    is_active: Optional[bool] = None


class DiscountCodeBase(BaseModel):
    code: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)
    discount_percent: int = Field(ge=1, le=100)
    product_id: Optional[str] = Field(default=None, min_length=1, max_length=50)
    customer_id: Optional[str] = Field(default=None, min_length=1, max_length=50)
    usage_limit: int = Field(default=1, ge=1)
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True


class DiscountCodeCreate(DiscountCodeBase):
    pass


class DiscountCodeUpdate(BaseModel):
    code: Optional[str] = Field(default=None, min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)
    discount_percent: Optional[int] = Field(default=None, ge=1, le=100)
    product_id: Optional[str] = Field(default=None, max_length=50)
    customer_id: Optional[str] = Field(default=None, max_length=50)
    usage_limit: Optional[int] = Field(default=None, ge=1)
    used_count: Optional[int] = Field(default=None, ge=0)
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class DiscountCodeResponse(BaseModel):
    discount_code_id: str
    code: str
    description: Optional[str] = None
    discount_percent: int
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    usage_limit: int
    used_count: int
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime


class AdminProductCreate(ProductCreate):
    pass


class AdminProductUpdate(ProductUpdate):
    rating_avg: Optional[Decimal] = Field(default=None, ge=0, le=5)
    total_reviews: Optional[int] = Field(default=None, ge=0)
