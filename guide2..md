# Hướng dẫn đọc thư mục `backend/` (dành cho người mới bắt đầu)

Tài liệu này giải thích toàn bộ thư mục `backend/` từ đầu tới cuối: **từng folder, từng file**, và các **framework/thư viện** dùng để làm gì — theo cách đơn giản để người mới học CNTT cũng hiểu.

---

## 1) Backend là gì? (nói dễ hiểu)

Hãy tưởng tượng bạn có một **cửa hàng online**:

- **Frontend** (giao diện): trang web/app mà người dùng bấm nút, xem sản phẩm.
- **Backend** (hậu trường): nơi xử lý nghiệp vụ:
  - đăng ký/đăng nhập
  - xem danh sách sản phẩm
  - tạo đơn hàng
  - lưu dữ liệu vào database
  - kiểm tra quyền (ai được làm gì)

Trong dự án này, backend là một **dịch vụ web API**: frontend gọi API bằng HTTP (GET/POST/PUT/DELETE), backend trả JSON.

---

## 2) Framework/thư viện đang dùng (và tại sao cần)

Bạn có thể xem danh sách trong `backend/requirements.txt`.

### 2.1 FastAPI (framework web)
- Dùng để tạo API nhanh, rõ ràng.
- Bạn sẽ thấy trong code: `FastAPI`, `APIRouter`, `Depends`.
- Nơi khởi tạo app: `backend/app/main.py`.

### 2.2 Uvicorn (server chạy FastAPI)
- FastAPI là “ứng dụng”, còn Uvicorn là “máy chủ” để chạy ứng dụng đó.
- Thường chạy kiểu: `uvicorn app.main:app --reload` (ví dụ minh hoạ).

### 2.3 SQLAlchemy (ORM: làm việc với database bằng Python)
- ORM giúp bạn thao tác database bằng object/class thay vì viết SQL thủ công.
- **Model** (bảng DB) nằm ở: `backend/app/models/*.py`.
- Kết nối DB nằm ở: `backend/app/database.py`.

### 2.4 Psycopg2-binary (driver PostgreSQL)
- “Driver” là cầu nối để Python kết nối PostgreSQL.

### 2.5 Alembic (migration: quản lý thay đổi cấu trúc DB)
- Khi bạn thêm cột mới, tạo bảng mới… Alembic giúp tạo “bản nâng cấp” DB có kiểm soát.
- Thư mục migration: `backend/alembic/` và các file trong `backend/alembic/versions/`.

### 2.6 Pydantic (schema/validate dữ liệu)
- Giúp kiểm tra dữ liệu request/response:
  - Ví dụ: email phải đúng định dạng, số lượng phải >= 1, v.v.
- Nằm ở: `backend/app/schemas/*.py`.

### 2.7 python-dotenv (đọc biến môi trường từ `.env`)
- File `.env` chứa cấu hình nhạy cảm (DB URL, SECRET_KEY).
- Đọc ở: `backend/app/config.py` và `backend/alembic/env.py`.

### 2.8 JWT (python-jose) + passlib/bcrypt (mã hoá mật khẩu)
- **JWT**: token dùng để xác thực (đăng nhập xong mới gọi được API cần quyền).
- **bcrypt**: hash mật khẩu (không lưu mật khẩu thô).
- JWT:
  - Customer: `backend/app/core/customer_auth.py`
  - Admin: `backend/Admin/admin_auth.py`
- Password hashing/verify:
  - `backend/app/services/customer_service.py`

### 2.9 pytest (test tự động)
- Chạy test để biết backend có hoạt động đúng không.
- File test: `backend/test_smoke.py`

---

## 3) Cách backend được tổ chức (các “tầng”)

Bạn có thể đọc theo chuỗi sau (từ ngoài vào trong):

1. **Router (API endpoints)**: nhận request, kiểm tra quyền, gọi service
2. **Service (logic nghiệp vụ)**: xử lý quy tắc, gọi database
3. **Model (ORM)**: mô tả bảng trong DB
4. **Schema (Pydantic)**: mô tả dữ liệu vào/ra của API
5. **Core (phần dùng chung)**: config, auth, dependency, logging
6. **Alembic (migration)**: lịch sử thay đổi database

Tưởng tượng:
- Router là **quầy tiếp tân**: nhận yêu cầu.
- Service là **nhân viên xử lý**: làm việc thật.
- Model là **bản thiết kế kho**: dữ liệu lưu thế nào.
- Schema là **mẫu đơn**: điền gì được/không được.

---

## 4) Giải thích toàn bộ `backend/` từ đầu tới cuối

Dưới đây là “bản đồ” của thư mục `backend/` và từng file quan trọng.

### 4.1 `backend/.env`
- File cấu hình môi trường (thường chỉ dùng local/dev).
- Thường có:
  - `DATABASE_URL`: đường dẫn kết nối PostgreSQL
  - `SECRET_KEY`: khoá bí mật để ký JWT
- Lưu ý: không nên commit `.env` lên git nếu chứa bí mật thật.

### 4.2 `backend/requirements.txt`
- Danh sách thư viện Python cần cài.

### 4.3 `backend/alembic.ini`
- File cấu hình Alembic:
  - Alembic sẽ đọc DB URL từ biến môi trường (liên quan `.env`).

### 4.4 `backend/smoke_test.py`
- “Smoke test” = test nhanh xem hệ thống sống hay chết.
- Script này dùng `fastapi.testclient.TestClient` để gọi API như một client:
  - gọi `/` và `/test-db`
  - login admin
  - tạo category, payment method, customer
  - login customer
  - tạo product (admin)
  - tạo order (customer)
  - admin patch status đơn hàng

### 4.5 `backend/test_smoke.py`
- Test dạng pytest (tự động).
- Mục tiêu: kiểm tra vài chức năng tối thiểu (root, db, login…).

---

## 5) Thư mục `backend/app/` (trái tim của backend)

### 5.1 `backend/app/main.py` (điểm bắt đầu của API)
Bạn có thể coi đây là nơi “lắp ráp” toàn bộ hệ thống:

- Tạo `app = FastAPI(...)`
- Bật CORS (cho phép frontend gọi API từ trình duyệt)
- `include_router(...)` để gắn các router vào app
- Middleware log request:
  - gắn `X-Request-Id` và log thời gian xử lý
- Exception handler:
  - bắt lỗi và trả JSON lỗi thống nhất
- Có route:
  - `GET /` trả message “Backend is running”
  - `GET /test-db` thử query `SELECT 1`

### 5.2 `backend/app/config.py` (cấu hình)
- Đọc `.env` bằng `load_dotenv()`
- Tạo `settings` để code nơi khác dùng:
  - `settings.DATABASE_URL`
  - `settings.SECRET_KEY`

### 5.3 `backend/app/database.py` (kết nối DB)
- Tạo `engine` (kết nối tới PostgreSQL)
- Tạo `SessionLocal` (mỗi request thường dùng 1 session)
- Tạo `Base` để các model kế thừa

---

## 6) `backend/app/core/` (phần dùng chung)

### 6.1 `backend/app/core/dependencies.py`
- Có hàm `get_db()`:
  - tạo session DB
  - `yield` session cho router/service dùng
  - cuối cùng đóng session
- Đây là kỹ thuật thường dùng trong FastAPI gọi là **Dependency Injection**.

### 6.2 `backend/app/core/customer_auth.py`
- Chức năng:
  - tạo JWT token cho customer khi login (`create_customer_access_token`)
  - lấy customer hiện tại từ JWT (`get_current_customer`)
- `get_current_customer`:
  - đọc token từ header `Authorization: Bearer <token>`
  - giải mã, lấy `customer_id`
  - query DB để lấy `Customer`

### 6.3 `backend/app/core/logging_config.py`
- Chuyển logging sang dạng JSON (dễ đọc bằng tool, dễ lọc theo request id).
- Có `request_id_ctx` để mỗi request có một “mã” riêng.

---

## 7) `backend/app/models/` (các bảng trong database)

Mỗi file thường tương ứng 1 bảng DB (SQLAlchemy model).

### 7.1 `backend/app/models/__init__.py`
- Import tất cả model để:
  - Alembic có thể “nhìn thấy” toàn bộ bảng khi autogenerate migration.

### 7.2 Các model chính
- `backend/app/models/customer.py`: bảng `customers`
  - thông tin khách hàng, quan hệ: orders, reviews, addresses, wishlist
- `backend/app/models/category.py`: bảng `categories`
  - loại sản phẩm
- `backend/app/models/product.py`: bảng `products`
  - FK tới category, có giá/giảm giá/tồn kho/rating
- `backend/app/models/payment_method.py`: bảng `paymentmethods`
  - phương thức thanh toán
- `backend/app/models/order.py`: bảng `orders`
  - FK customer + payment_method, trạng thái đơn, phí ship, giảm giá
- `backend/app/models/order_item.py`: bảng `orderitems`
  - các dòng sản phẩm trong 1 order
- `backend/app/models/review.py`: bảng `reviews`
  - rating/comment cho product
- `backend/app/models/address.py`: bảng `addresses`
  - địa chỉ giao hàng của customer
- `backend/app/models/wishlist.py`: bảng `wishlists`
  - danh sách sản phẩm yêu thích

---

## 8) `backend/app/schemas/` (mẫu dữ liệu request/response)

Schema giúp “lọc” dữ liệu:
- client gửi sai kiểu → báo lỗi rõ ràng
- response trả ra ổn định → frontend dễ dùng

### 8.1 `backend/app/schemas/__init__.py`
- Re-export một số schema để import tiện hơn (hiện export: product/category/customer/order/review/address/wishlist).

### 8.2 Các schema theo module
- `backend/app/schemas/auth.py`: `TokenResponse` (access token)
- `backend/app/schemas/customer.py`: create/update/login/response cho customer
- `backend/app/schemas/category.py`: create/update/response cho category
- `backend/app/schemas/product.py`: create/update/response cho product
- `backend/app/schemas/payment_method.py`: create/update/response cho payment method
- `backend/app/schemas/order.py`: create/update/response cho order (kèm `items`)
- `backend/app/schemas/order_item.py`: schema cho order item (hiện ít dùng trực tiếp)
- `backend/app/schemas/review.py`: create/response cho review
- `backend/app/schemas/address.py`: create/response cho address
- `backend/app/schemas/wishlist.py`: create/response cho wishlist

---

## 9) `backend/app/services/` (xử lý nghiệp vụ)

Service là nơi làm việc chính: query DB, kiểm tra điều kiện, commit/rollback.

### 9.1 `backend/app/services/exceptions.py`
- Tạo các exception phổ biến:
  - 404 Not Found
  - 409 Already Exists
  - 400 Business Logic Error
  - 401 Validation/Auth error

### 9.2 Các service theo module
- `backend/app/services/customer_service.py`
  - tạo customer, authenticate (login), update, delete
  - hash/verify password (bcrypt; có fallback SHA256 và tự “nâng cấp” hash)
- `backend/app/services/category_service.py`: CRUD category
- `backend/app/services/product_service.py`: CRUD product (khi tạo phải có category tồn tại)
- `backend/app/services/payment_service.py`: CRUD payment method
- `backend/app/services/order_service.py`
  - tạo order + order items
  - kiểm tra customer/payment/items
  - lấy danh sách order theo customer
- `backend/app/services/review_service.py`
  - tạo review
  - cập nhật tổng review và rating trung bình cho product
- `backend/app/services/address_service.py`: tạo/lấy/xoá address
- `backend/app/services/wishlist_service.py`: add/list/remove wishlist

---

## 10) `backend/app/routers/` (các API endpoint)

Router là nơi định nghĩa URL:
- `/customers/...`
- `/products/...`
- `/orders/...`
v.v.

Mỗi router thường:
- nhận schema (Pydantic)
- có `db: Session = Depends(get_db)`
- có auth tuỳ endpoint:
  - admin token cho thao tác quản trị
  - customer token cho thao tác cá nhân

Danh sách:
- `backend/app/routers/customer_router.py`
  - tạo tài khoản
  - login (JSON)
  - token (OAuth2 form)
  - admin xem danh sách customers
  - customer xem/sửa/xoá chính mình
- `backend/app/routers/product_router.py`
  - xem danh sách, xem chi tiết
  - tạo/sửa/xoá (admin)
- `backend/app/routers/category_router.py`
  - xem danh sách, xem chi tiết
  - tạo/sửa/xoá (admin)
- `backend/app/routers/payment_router.py`
  - xem danh sách, xem chi tiết
  - tạo/sửa/xoá (admin)
- `backend/app/routers/order_router.py`
  - tạo order (customer)
  - list/get/delete (customer owner)
- `backend/app/routers/review_router.py`
  - tạo review (customer owner)
  - list theo product hoặc theo customer
- `backend/app/routers/address_router.py`
  - tạo/list/xoá address (customer owner)
- `backend/app/routers/wishlist_router.py`
  - thêm/list/xoá wishlist item (customer owner)

---

## 11) `backend/Admin/` (API cho quản trị viên)

Trong dự án này phần admin tách riêng ở thư mục `backend/Admin/`.

- `backend/Admin/admin_auth.py`
  - xác thực admin (đang hardcode username/password)
  - tạo token JWT
  - `get_current_admin()` để bảo vệ endpoint admin
- `backend/Admin/admin_schema.py`
  - schema response login admin
- `backend/Admin/admin_service.py`
  - “điều phối” sang các service sẵn có của app (product_service, order_service)
  - cập nhật status order
- `backend/Admin/admin_router.py`
  - `/admin/login`
  - quản lý products
  - quản lý orders + patch status

---

## 12) `backend/alembic/` (migration database)

Bạn sẽ gặp 3 phần chính:

### 12.1 `backend/alembic/env.py`
- Nạp `.env`, set `sqlalchemy.url`, load `Base.metadata`.
- Giúp Alembic biết “mô hình DB hiện tại” dựa trên models.

### 12.2 `backend/alembic/script.py.mako`
- Template dùng khi tạo migration mới.

### 12.3 `backend/alembic/versions/*.py`
- Mỗi file là một “bước thay đổi DB” (upgrade/downgrade).
- Ví dụ:
  - `b74ea..._initial_migration.py`: tạo bảng ban đầu
  - `c3d4e..._expand_retail_schema.py`: thêm reviews/addresses/wishlists + thêm cột
  - `f1a2b..._add_fk_indexes_for_performance.py`: thêm index
  - `a1b2c..._convert_ids_to_varchar...py`: chuyển PK/FK sang dạng chuỗi (varchar)

---

## 13) Một ví dụ “đọc theo đường đi của request”

Ví dụ “admin tạo sản phẩm”:

1. Client gọi `POST /products/` kèm token admin
2. Router: `backend/app/routers/product_router.py`
   - kiểm tra token admin qua `Depends(get_current_admin)`
   - lấy DB session qua `Depends(get_db)`
3. Service: `backend/app/services/product_service.py`
   - check category tồn tại
   - tạo `Product` và commit
4. Model: `backend/app/models/product.py` map vào bảng `products`
5. Schema: `backend/app/schemas/product.py` quyết định dữ liệu request/response

---

## 14) Gợi ý cho người mới học (bạn nên học theo thứ tự)

1. Hiểu HTTP cơ bản: GET/POST/PUT/DELETE, status code (200/201/401/403/404/500)
2. Mở `backend/app/main.py` để thấy “app được lắp như thế nào”
3. Chọn 1 tính năng nhỏ (ví dụ login customer) và đọc theo chuỗi:
   - `routers/customer_router.py` → `services/customer_service.py` → `models/customer.py` → `schemas/customer.py`
4. Hiểu `.env` và `config.py` (vì mọi thứ phụ thuộc DB/SECRET_KEY)
5. Chạy smoke test (`backend/smoke_test.py`) để thấy luồng API thực tế

