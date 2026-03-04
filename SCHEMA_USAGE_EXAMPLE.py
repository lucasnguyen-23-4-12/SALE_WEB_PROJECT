"""
EXAMPLE: Cách sử dụng Schemas trong FastAPI Endpoints
=====================================

Đây là hướng dẫn chi tiết về cách dùng schemas đã tạo trong PHASE 5
để xây dựng API endpoints (PHASE 6).
"""

# ===================== EXAMPLE 1: PRODUCT ROUTER =====================

# ✅ File: backend/app/routers/product.py

from fastapi import APIRouter, HTTPException, Depends
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product as ProductModel
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


# ✅ CREATE - Tạo product mới
@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,  # 👈 Dùng ProductCreate schema
    db: Session = Depends(get_db)
):
    """
    Tạo product mới
    
    Request body:
    {
        "product_name": "Laptop Dell",
        "description": "High performance",
        "image_url": "https://...",
        "unit_price": 1500.00,
        "category_id": 1
    }
    
    Response:
    {
        "product_id": 1,
        "product_name": "Laptop Dell",
        "description": "High performance",
        "image_url": "https://...",
        "unit_price": 1500.00,
        "category_id": 1
    }
    """
    # ProductCreate schema tự động validate dữ liệu
    # - Check required fields
    # - Check type (unit_price phải Decimal)
    # - Check category_id là int
    
    new_product = ProductModel(
        product_name=product_data.product_name,
        description=product_data.description,
        image_url=product_data.image_url,
        unit_price=product_data.unit_price,
        category_id=product_data.category_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    # ProductResponse schema sẽ convert ORM object thành dict
    # Sử dụng model_validate với from_attributes=True
    return new_product  # ✅ Auto convert to ProductResponse


# ✅ READ - Lấy product theo ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Lấy product theo ID
    
    Response:
    {
        "product_id": 1,
        "product_name": "Laptop Dell",
        "description": "High performance",
        "image_url": "https://...",
        "unit_price": 1500.00,
        "category_id": 1
    }
    """
    product = db.query(ProductModel).filter(
        ProductModel.product_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product  # ✅ ORM object auto convert to ProductResponse schema


# ✅ READ ALL - Lấy tất cả products
@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách products (paginated)
    
    Response:
    [
        {
            "product_id": 1,
            "product_name": "Laptop Dell",
            "description": "High performance",
            "image_url": "https://...",
            "unit_price": 1500.00,
            "category_id": 1
        },
        ...
    ]
    """
    products = db.query(ProductModel).offset(skip).limit(limit).all()
    return products  # ✅ List of ORM objects auto convert to List[ProductResponse]


# ✅ UPDATE - Cập nhật product
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,  # 👈 Dùng ProductUpdate schema (all optional)
    db: Session = Depends(get_db)
):
    """
    Cập nhật product
    
    Có thể update một hoặc nhiều fields:
    {
        "product_name": "Laptop Dell 15"
    }
    
    hoặc
    
    {
        "product_name": "Laptop Dell 15",
        "unit_price": 1600.00,
        "category_id": 2
    }
    
    Response:
    {
        "product_id": 1,
        "product_name": "Laptop Dell 15",
        "description": "High performance",
        "image_url": "https://...",
        "unit_price": 1600.00,
        "category_id": 2
    }
    """
    product = db.query(ProductModel).filter(
        ProductModel.product_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # ProductUpdate schema cho phép update một phần
    # Chỉ update fields không None
    if product_data.product_name is not None:
        product.product_name = product_data.product_name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.image_url is not None:
        product.image_url = product_data.image_url
    if product_data.unit_price is not None:
        product.unit_price = product_data.unit_price
    if product_data.category_id is not None:
        product.category_id = product_data.category_id
    
    db.commit()
    db.refresh(product)
    
    return product  # ✅ Auto convert to ProductResponse


# ✅ DELETE - Xoá product
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Xoá product
    """
    product = db.query(ProductModel).filter(
        ProductModel.product_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    
    return {"message": "Product deleted successfully"}


# ===================== EXAMPLE 2: CUSTOMER ROUTER =====================

# ✅ File: backend/app/routers/customer.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer as CustomerModel
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer_data: CustomerCreate,  # 👈 CustomerCreate có password field
    db: Session = Depends(get_db)
):
    """
    Tạo customer mới
    
    Request body:
    {
        "customer_name": "Nguyen Van A",
        "customer_email": "a@gmail.com",  # ✅ EmailStr validation tự động
        "phone_number": "0912345678",
        "address": "123 Main St",
        "password": "securepass123"
    }
    
    Response:
    {
        "customer_id": 1,
        "customer_name": "Nguyen Van A",
        "customer_email": "a@gmail.com",
        "phone_number": "0912345678",
        "address": "123 Main St",
        "created_at": "2026-03-03"
    }
    """
    # ✅ EmailStr validation tự động
    # Nếu email không hợp lệ, FastAPI sẽ raise ValidationError
    
    # Hash password (don't store plain text!)
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(customer_data.password)
    
    new_customer = CustomerModel(
        customer_name=customer_data.customer_name,
        customer_email=customer_data.customer_email,
        phone_number=customer_data.phone_number,
        address=customer_data.address,
        password_hash=hashed_password
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return new_customer


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,  # 👈 Không có password field
    db: Session = Depends(get_db)
):
    """
    Cập nhật customer
    
    ⚠️ Chú ý: CustomerUpdate KHÔNG có password field
    
    Request body:
    {
        "customer_name": "Nguyen Van B",
        "phone_number": "0987654321"
    }
    
    Để đổi password, cần endpoint riêng (PHASE 6 advanced)
    """
    customer = db.query(CustomerModel).filter(
        CustomerModel.customer_id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Update chỉ fields không None
    if customer_data.customer_name is not None:
        customer.customer_name = customer_data.customer_name
    if customer_data.phone_number is not None:
        customer.phone_number = customer_data.phone_number
    if customer_data.address is not None:
        customer.address = customer_data.address
    # ⚠️ password không update ở đây
    
    db.commit()
    db.refresh(customer)
    
    return customer


# ===================== EXAMPLE 3: ORDER ROUTER =====================

# ✅ File: backend/app/routers/order.py

# ... Tương tự như Product

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,  # 👈 OrderCreate schema
    db: Session = Depends(get_db)
):
    """
    Tạo order mới
    
    Request body:
    {
        "customer_id": 1,
        "payment_method_id": 1,
        "order_date": "2026-03-03",
        "status": "pending"
    }
    
    ✅ ValidationError nếu:
    - customer_id không phải int
    - payment_method_id không phải int
    - order_date không phải date
    - status không phải string
    """
    pass


# ===================== KEY CONCEPTS =====================

"""
1️⃣ SCHEMA DÙNG CHO SIDE NÀO?

   CLIENT SEND                    SERVER RETURN
   ↓                              ↓
   ProductCreate                  ProductResponse
   ProductUpdate                  OrderResponse
   ↓                              ↓
   POST /products                 GET /products/{id}
   PUT /products/{id}             POST /products (response)


2️⃣ VALIDATION TỰ ĐỘNG

   @router.post("/")
   def create(data: ProductCreate):  # ✅ FastAPI tự động validate
       # Nếu data invalid → 422 Unprocessable Entity
       # Nếu data valid → tiếp tục xử lý
       pass


3️⃣ ORM MODE - AUTO CONVERT

   product = db.query(Product).first()  # ORM object
   return product  # ✅ FastAPI auto convert to ProductResponse
                   #    Dùng model_validate(from_attributes=True)


4️⃣ EMAIL VALIDATION

   from pydantic import EmailStr
   
   customer_email: EmailStr  # ✅ Auto validate
   
   # ❌ "not-an-email" → ValidationError
   # ✅ "user@example.com" → OK


5️⃣ DECIMAL CHO TIỀN TỆ

   from decimal import Decimal
   
   unit_price: Decimal  # ✅ Chính xác cho tiền tệ
   
   # Nhân, chia không mất precision
   total = Decimal('1500.00') * 2  # 3000.00 (chính xác)


6️⃣ OPTIONAL FIELDS CHO UPDATE

   class ProductUpdate(BaseModel):
       product_name: Optional[str] = None
       
   # ✅ Cho phép update một phần
   data = ProductUpdate(product_name="new name")  # OK
   data = ProductUpdate()  # OK - all None
   data = ProductUpdate(product_name=None)  # OK


7️⃣ ERROR HANDLING

   if not product:
       raise HTTPException(status_code=404, detail="Not found")
   
   # FastAPI auto return:
   # {"detail": "Not found"}
"""

# ===================== TEST CÁC ENDPOINTS =====================

"""
CURL EXAMPLES:

1️⃣ CREATE Product:
   curl -X POST "http://localhost:8000/products/" \
   -H "Content-Type: application/json" \
   -d '{
     "product_name": "Laptop Dell",
     "description": "High performance",
     "image_url": "https://...",
     "unit_price": 1500.00,
     "category_id": 1
   }'


2️⃣ GET Product:
   curl "http://localhost:8000/products/1"


3️⃣ UPDATE Product:
   curl -X PUT "http://localhost:8000/products/1" \
   -H "Content-Type: application/json" \
   -d '{
     "product_name": "Laptop Dell 15",
     "unit_price": 1600.00
   }'


4️⃣ DELETE Product:
   curl -X DELETE "http://localhost:8000/products/1"


5️⃣ CREATE Customer (Invalid Email):
   curl -X POST "http://localhost:8000/customers/" \
   -H "Content-Type: application/json" \
   -d '{
     "customer_name": "Test",
     "customer_email": "not-an-email",
     "password": "123456"
   }'
   
   Response:
   {
     "detail": [
       {
         "type": "value_error",
         "loc": ["body", "customer_email"],
         "msg": "value is not a valid email address: ...",
         "input": "not-an-email"
       }
     ]
   }
"""
