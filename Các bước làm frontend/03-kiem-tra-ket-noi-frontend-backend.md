# Kiểm Tra Kết Nối Frontend ↔ Backend

## 1. Đã kiểm tra những gì
- Đã quét toàn bộ source backend chính trong:
  - `backend/app/main.py`
  - `backend/app/routers/*`
  - `backend/app/services/*`
  - `backend/app/schemas/*`
  - `backend/app/models/*`
  - `backend/app/core/*`
  - `backend/Admin/*`
  - `backend/.env`, `backend/requirements.txt`
- Đã đối chiếu với toàn bộ call API hiện có trong `frontend/js/*`.

## 2. Các API backend hiện có

### 2.1 Customers (`/customers`)
- `POST /customers/` tạo customer
- `POST /customers/register/request-otp` gửi OTP email
- `POST /customers/register/with-otp` đăng ký với OTP
- `POST /customers/login` đăng nhập customer
- `POST /customers/google` đăng nhập/đăng ký Google
- `POST /customers/token` OAuth2 token form
- `GET /customers/` (admin)
- `GET /customers/{customer_id}` (owner)
- `PUT /customers/{customer_id}` (owner)
- `DELETE /customers/{customer_id}` (owner)

### 2.2 Admin (`/admin`)
- `POST /admin/login`
- `GET /admin/me` (check token admin)
- `GET /admin/products`
- `GET /admin/products/{product_id}`
- `POST /admin/products`
- `PUT /admin/products/{product_id}`
- `DELETE /admin/products/{product_id}`
- `GET /admin/orders`
- `GET /admin/orders/{order_id}`
- `PATCH /admin/orders/{order_id}/status`

### 2.3 Public/Domain APIs
- Products: `/products` (CRUD, create/update/delete cần admin)
- Categories: `/categories` (CRUD, create/update/delete cần admin)
- Payment methods: `/payment-methods` (CRUD, create/update/delete cần admin)
- Orders: `/orders` (customer auth)
- Addresses: `/addresses` (customer auth)
- Reviews: `/reviews` (customer auth khi tạo/xem theo customer)
- Wishlists: `/wishlists` (customer auth)

## 3. Frontend đang kết nối backend đến đâu

### 3.1 Đã kết nối thật
- `frontend/js/auth/login.js`
  - `POST /admin/login`
  - `POST /customers/login`
  - `POST /customers/google`
- `frontend/js/auth/register.js`
  - `POST /customers/register/request-otp`
  - `POST /customers/register/with-otp`
  - `POST /customers/google`
- `frontend/js/admin/admin.js`
  - `GET /admin/me` để xác minh quyền admin

### 3.2 Chưa kết nối (đang tĩnh hoặc localStorage)
- Products page, product detail: chưa gọi `/products`, `/categories`
- Cart + Checkout: chưa tạo order thật qua `/orders`
- All orders + order detail: đang dùng `orders-data.js` mock
- Profile: chưa gọi `GET/PUT /customers/{id}`
- Address page: chưa gọi `/addresses`
- Password page: chưa có API đổi mật khẩu
- Product reviews page: chưa gọi `/reviews`
- Notification: chưa có API dữ liệu
- Wishlist: backend có API nhưng frontend chưa có màn hình gọi `/wishlists`
- Admin dashboard: mới check quyền, chưa load dữ liệu thật từ `/admin/orders`, `/admin/products`

## 4. Nhận xét quan trọng khi nối thêm

### 4.1 Token/định danh customer
- Backend đang trả JWT customer với `sub = customer_id`.
- Frontend hiện chưa decode token để lấy `customer_id`.
- Muốn gọi các API owner như `/customers/{customer_id}`, `/addresses/customer/{customer_id}`, `/orders/...` cần có `customer_id`.

Gợi ý:
- Cách tốt nhất: thêm endpoint `GET /customers/me` trả profile từ token.
- Cách tạm: decode JWT ở frontend để lấy `sub` (customer_id).

### 4.2 Order detail cho UI hiện tại
- `OrderResponse` hiện chưa chứa danh sách `order_items`.
- UI “chi tiết đơn hàng” cần tên sản phẩm, số lượng, trạng thái từng item.

Gợi ý:
- Thêm `GET /orders/{order_id}/items` hoặc mở rộng `OrderResponse` include `items`.

### 4.3 Admin login form
- Backend admin nhận `username/password` theo OAuth2 form.
- Frontend đang gửi đúng `application/x-www-form-urlencoded`.
- Hiện đã cho phép admin đăng nhập bằng `admin@tamtai.vn` hoặc `admin`.

### 4.4 CORS
- Backend đã mở CORS cho:
  - `http://127.0.0.1:5500`
  - `http://localhost:5500`
- Phù hợp chạy frontend local với Live Server.

## 5. Checklist ưu tiên nối API tiếp theo

### Ưu tiên 1 (nên làm ngay)
- Tạo `GET /customers/me`
- Nối Profile:
  - `GET /customers/me`
  - `PUT /customers/{customer_id}`
- Nối Products:
  - `GET /products`
  - `GET /products/{id}`

### Ưu tiên 2
- Nối Cart/Checkout/Orders:
  - `GET /payment-methods`
  - `POST /orders`
  - `GET /orders`
  - `GET /orders/{id}`
- Bổ sung backend order details (`items`) để render trang chi tiết đơn

### Ưu tiên 3
- Nối Address:
  - `POST /addresses`
  - `GET /addresses/customer/{customer_id}`
  - `DELETE /addresses/{id}`
- Nối Reviews:
  - `POST /reviews`
  - `GET /reviews/product/{id}`
  - `GET /reviews/customer/{customer_id}`
- Nối Admin dashboard data:
  - `GET /admin/orders`
  - `GET /admin/products`

## 6. Kết luận nhanh
- Hệ thống hiện **đã có khung backend đầy đủ** và frontend **đã nối auth tốt**.
- Phần nghiệp vụ chính (products/cart/orders/profile/address/review/admin data) **chưa nối API thật**, mới dùng dữ liệu tĩnh.
- Có thể triển khai nối thật theo checklist trên mà không cần đổi kiến trúc lớn.
