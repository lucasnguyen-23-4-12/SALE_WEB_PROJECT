# Sale_Web_Project — Guide kiến trúc (Backend)

Tài liệu này giúp bạn “đọc” nhanh toàn bộ `backend/`: kiến trúc, các tầng (layers), vai trò từng folder/từng file, và luồng request end-to-end.

> Phạm vi: mô tả theo trạng thái code hiện tại trong repo (ngày 2026-03-11).

## 1) Tổng quan cấu trúc repo

```
Sale_Web_Project/
  backend/            # FastAPI + SQLAlchemy + Alembic
  frontend_demo/      # HTML/CSS/JS demo gọi API
  frontend/           # (hiện chỉ có demo.py)
  venv/               # virtualenv (không commit/không mô tả chi tiết)
  *.md                # tài liệu/plan khác (QUICK_START, CHECKLIST, ...)
```

## 2) Kiến trúc backend (tầng/layer)

Backend đang theo mô hình “Router → Service → DB(Model)” với các lớp phụ trợ (core) cho logging/auth/DI:

- **API layer (Presentation)**: `backend/app/routers/*.py` + `backend/Admin/admin_router.py`
  - Khai báo endpoint, validate input (Pydantic schema), inject dependency (`Depends`), check quyền (customer/admin), trả response.
- **Service layer (Application/Business)**: `backend/app/services/*.py` + `backend/Admin/admin_service.py`
  - Chứa logic nghiệp vụ/CRUD, thao tác `Session` (SQLAlchemy), raise exception nghiệp vụ.
- **Schema layer (DTO/Validation)**: `backend/app/schemas/*.py` + `backend/Admin/admin_schema.py`
  - Pydantic models cho request/response; dùng `from_attributes=True` để serialize từ ORM model.
- **Data layer (Persistence)**: `backend/app/models/*.py`, `backend/app/database.py`
  - SQLAlchemy ORM models map tới các bảng (customers, orders, products, …), quan hệ (relationship), engine/session.
- **Core/Cross-cutting**: `backend/app/core/*.py`, `backend/app/config.py`
  - Config từ `.env`, dependency `get_db`, auth JWT cho customer/admin, logging JSON + request_id.
- **Migrations**: `backend/alembic/` + `backend/alembic.ini`
  - Quản lý schema DB và thay đổi schema theo thời gian.

## 3) Sơ đồ kiến trúc (Mermaid)

```mermaid
flowchart LR
  Client[Frontend Demo / API Client] -->|HTTP| FastAPI[FastAPI app<br/>backend/app/main.py]

  FastAPI --> Routers[Routers<br/>backend/app/routers/*.py]
  FastAPI --> AdminRouter[Admin Router<br/>backend/Admin/admin_router.py]

  Routers -->|Depends|getdb[get_db()<br/>backend/app/core/dependencies.py]
  AdminRouter -->|Depends|getdb

  Routers --> AuthCustomer[get_current_customer()<br/>backend/app/core/customer_auth.py]
  AdminRouter --> AuthAdmin[get_current_admin()<br/>backend/Admin/admin_auth.py]

  Routers --> Services[Services<br/>backend/app/services/*.py]
  AdminRouter --> AdminService[Admin service<br/>backend/Admin/admin_service.py]

  Services --> ORM[SQLAlchemy ORM Models<br/>backend/app/models/*.py]
  AdminService --> ORM

  ORM --> DB[(PostgreSQL)]
  Alembic[Alembic migrations<br/>backend/alembic/] --> DB

  FastAPI --> Logging[JSON logging + request_id<br/>backend/app/core/logging_config.py]
```

## 4) Luồng xử lý request (cách “đọc” code nhanh)

Ví dụ luồng “tạo order”:

1. **Route**: `backend/app/routers/order_router.py` nhận `OrderCreate` (schema), inject `db = Depends(get_db)`, inject `current_customer = Depends(get_current_customer)`.
2. **Auth/Permission**:
   - `get_current_customer()` decode JWT (`Authorization: Bearer ...`) → trả ORM `Customer`.
   - Router check `current_customer.customer_id == payload.customer_id`.
3. **Service**: gọi `backend/app/services/order_service.py:create_order()`
   - validate tồn tại Customer/PaymentMethod, validate item list, tính tiền, tạo `Order` + `OrderItem`, commit.
4. **Response**: ORM `Order` được FastAPI serialize sang `OrderResponse` nhờ `from_attributes=True`.
5. **Logging & Error**:
   - Middleware trong `backend/app/main.py` gắn `X-Request-Id`, log JSON `request`.
   - Exception handlers chuẩn hoá payload lỗi.

## 5) AuthN/AuthZ (customer vs admin)

- **Customer**: JWT trong `backend/app/core/customer_auth.py`
  - Token URL: `/customers/token` (OAuth2PasswordBearer), ngoài ra có `/customers/login` (JSON login).
  - Payload token có `sub=<customer_id>` và `role=customer`.
- **Admin**: JWT trong `backend/Admin/admin_auth.py`
  - Token URL: `/admin/login`
  - Admin credential đang hardcode: `admin/admin123` (phục vụ dev/test).

## 6) Database & migration

- Kết nối DB: `backend/app/config.py` đọc `.env` → `settings.DATABASE_URL`.
- SQLAlchemy:
  - Engine/session/base: `backend/app/database.py` (`engine`, `SessionLocal`, `Base`).
  - ORM models: `backend/app/models/*.py` (map cột DB kiểu `"CustomerID"`, `"OrderID"`, …).
- Alembic:
  - Config: `backend/alembic.ini` (đặt `sqlalchemy.url` từ env var).
  - Env: `backend/alembic/env.py` load `.env`, import `Base` + `app.models` để autogenerate metadata.
  - Migrations trong `backend/alembic/versions/`.

Ghi chú quan trọng về ID:
- ORM hiện dùng `String(50)` cho các PK/FK và `server_default=FetchedValue()` (DB tự sinh giá trị).
- Có migration `a1b2c3d4e5f6...` chuyển nhiều PK/FK từ `INT` sang `VARCHAR` và giữ default sequence dạng text.

## 7) Giải thích chi tiết theo folder/file

> Không liệt kê các file sinh tự động như `__pycache__/`, `.pytest_cache/`.

### 7.1) `backend/` (root backend)

- `backend/.env`: biến môi trường local (ít nhất: `DATABASE_URL`, `SECRET_KEY`).
- `backend/requirements.txt`: dependencies (FastAPI, SQLAlchemy, Alembic, JWT, bcrypt, pytest, ...).
- `backend/alembic.ini`: cấu hình Alembic (script location, logging, `sqlalchemy.url` lấy từ env).
- `backend/smoke_test.py`: script smoke test end-to-end bằng `TestClient` (tạo category/payment/customer/product/order, patch status admin).
- `backend/test_smoke.py`: pytest smoke tests cơ bản (root, test-db, admin login, customer login + protected route).

### 7.2) `backend/app/` (application package)

- `backend/app/main.py`: entrypoint FastAPI
  - cấu hình CORS, include routers, middleware logging, exception handlers, route `/` và `/test-db`.
- `backend/app/config.py`: load `.env`, expose `settings.DATABASE_URL`, `settings.SECRET_KEY`.
- `backend/app/database.py`: tạo `engine`, `SessionLocal`, `Base` cho ORM.

#### 7.2.1) `backend/app/core/` (cross-cutting)

- `backend/app/core/__init__.py`: marker package.
- `backend/app/core/dependencies.py`: `get_db()` tạo/đóng SQLAlchemy `Session` (FastAPI dependency).
- `backend/app/core/customer_auth.py`: JWT auth cho customer (`create_customer_access_token`, `get_current_customer`).
- `backend/app/core/logging_config.py`: JSON logging + `request_id` contextvar (`configure_json_logging`).

#### 7.2.2) `backend/app/models/` (SQLAlchemy ORM models)

- `backend/app/models/__init__.py`: import tất cả model để tiện load metadata.
- `backend/app/models/customer.py`: bảng `customers`, quan hệ orders/reviews/addresses/wishlist.
- `backend/app/models/category.py`: bảng `categories`, quan hệ products.
- `backend/app/models/product.py`: bảng `products`, FK category + quan hệ order_items/reviews/wishlists.
- `backend/app/models/payment_method.py`: bảng `paymentmethods`, quan hệ orders.
- `backend/app/models/order.py`: bảng `orders`, FK customer/payment_method + quan hệ order_items.
- `backend/app/models/order_item.py`: bảng `orderitems`, FK order/product.
- `backend/app/models/review.py`: bảng `reviews`, FK product/customer.
- `backend/app/models/address.py`: bảng `addresses`, FK customer.
- `backend/app/models/wishlist.py`: bảng `wishlists`, FK customer/product.

#### 7.2.3) `backend/app/schemas/` (Pydantic schemas)

- `backend/app/schemas/__init__.py`: re-export một số schema bằng wildcard import (hiện gồm: product/category/customer/order/review/address/wishlist; không gồm `auth.py`, `payment_method.py`, `order_item.py`).
- `backend/app/schemas/auth.py`: `TokenResponse` (access_token, token_type).
- `backend/app/schemas/customer.py`: `CustomerCreate/Update/Response/Login`.
- `backend/app/schemas/category.py`: `CategoryCreate/Update/Response`.
- `backend/app/schemas/product.py`: `ProductCreate/Update/Response`.
- `backend/app/schemas/payment_method.py`: `PaymentMethodCreate/Update/Response`.
- `backend/app/schemas/order.py`: `OrderCreate/Update/Response` + `OrderItemInput`.
- `backend/app/schemas/order_item.py`: `OrderItemCreate/Response` (hiện chủ yếu phục vụ typing).
- `backend/app/schemas/review.py`: `ReviewCreate/Response`.
- `backend/app/schemas/address.py`: `AddressCreate/Response`.
- `backend/app/schemas/wishlist.py`: `WishlistCreate/Response`.

#### 7.2.4) `backend/app/services/` (business logic)

- `backend/app/services/__init__.py`: import/điều hướng các service module.
- `backend/app/services/exceptions.py`: exception chuẩn hoá (404/409/400/401) dựa trên `HTTPException`.
- `backend/app/services/customer_service.py`: CRUD customer + hash/verify password (bcrypt + fallback SHA256 và auto-migrate hash).
- `backend/app/services/category_service.py`: CRUD category.
- `backend/app/services/product_service.py`: CRUD product (validate tồn tại category khi tạo).
- `backend/app/services/payment_service.py`: CRUD payment method.
- `backend/app/services/order_service.py`: tạo order + order items, validate customer/payment/items, truy vấn orders theo customer.
- `backend/app/services/review_service.py`: CRUD review, cập nhật aggregate rating/total_reviews cho product.
- `backend/app/services/address_service.py`: CRUD address theo customer.
- `backend/app/services/wishlist_service.py`: CRUD wishlist theo customer.

#### 7.2.5) `backend/app/routers/` (FastAPI routers)

- `backend/app/routers/__init__.py`: (trống) package marker.
- `backend/app/routers/customer_router.py`: `/customers/*` (create, login, token OAuth form, list (admin), get/update/delete (self)).
- `backend/app/routers/category_router.py`: `/categories/*` (CRUD; create/update/delete require admin).
- `backend/app/routers/product_router.py`: `/products/*` (CRUD; write require admin).
- `backend/app/routers/payment_router.py`: `/payment-methods/*` (CRUD; write require admin).
- `backend/app/routers/order_router.py`: `/orders/*` (create/list/get/delete; require customer token và giới hạn theo owner).
- `backend/app/routers/review_router.py`: `/reviews/*` (create require owner; list theo product/customer).
- `backend/app/routers/address_router.py`: `/addresses/*` (create/list/delete theo customer owner).
- `backend/app/routers/wishlist_router.py`: `/wishlists/*` (add/list/delete theo customer owner).

#### 7.2.6) `backend/app/utils/`

- `backend/app/utils/__init__.py`: hiện chưa có utility cụ thể (placeholder).

### 7.3) `backend/Admin/` (module admin)

- `backend/Admin/admin_auth.py`: JWT auth cho admin + `authenticate_admin()` (hardcode credential).
- `backend/Admin/admin_schema.py`: schema login admin (`AdminLoginRequest/Response`).
- `backend/Admin/admin_service.py`: wrapper service cho admin (quản lý products, orders; patch status order).
- `backend/Admin/admin_router.py`: router `/admin/*` (login, quản lý product/order; require admin token).

### 7.4) `backend/alembic/` (migrations)

- `backend/alembic/README`: mô tả chung (default).
- `backend/alembic/script.py.mako`: template file migration.
- `backend/alembic/env.py`: nạp `.env`, set DB URL cho alembic, load `Base.metadata`.
- `backend/alembic/versions/b74ea1262042_initial_migration.py`: migration khởi tạo bảng/index cơ bản.
- `backend/alembic/versions/c3d4e5f6add_expand_retail_schema.py`: mở rộng schema (thêm reviews/addresses/wishlists, thêm cột product/order/customer).
- `backend/alembic/versions/d7f0a1b2c3d4_fix_products_category_not_null.py`: backfill `products.Category` NULL và enforce NOT NULL.
- `backend/alembic/versions/e9c1d2e3f4a5_enforce_orders_required_fields_not_null.py`: enforce NOT NULL cho các field bắt buộc của `orders`.
- `backend/alembic/versions/f1a2b3c4d5e6_add_fk_indexes_for_performance.py`: thêm index cho FK/field filter phổ biến.
- `backend/alembic/versions/a1b2c3d4e5f6_convert_ids_to_varchar_and_tighten_constraints.py`: chuyển PK/FK sang `VARCHAR`, drop/recreate indexes/constraints tương ứng.

## 8) Gợi ý cải thiện (để bạn đọc/scale dễ hơn)

- Tách rõ “Admin module” vào `backend/app/admin/` (thay vì `backend/Admin/`) để tránh import path lạ.
- Tránh `from app.models import *` / `from app.schemas.product import *` trong `__init__.py` nếu repo lớn dần (dễ tạo vòng import và khó đọc).
- Tách “repository/data access” layer (nếu logic query phức tạp) thay vì để dồn trong `services/`.
