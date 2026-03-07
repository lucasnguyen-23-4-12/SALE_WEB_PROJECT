# KẾ HOẠCH PHÁT TRIỂN BACKEND ADMIN

Project: SALE_WEB_PROJECT  
Phụ trách: Lê Huỳnh Tấn Đạt  
Module: Admin Backend

---

# 1. MỤC TIÊU MODULE ADMIN

Xây dựng hệ thống API cho Admin để quản trị website bán hàng.

Admin có quyền:

- Quản lý sản phẩm
- Quản lý đơn hàng
- Xem thông tin khách hàng
- Kiểm soát hoạt động của hệ thống

Module này chỉ phục vụ cho **Admin Panel**, không dùng cho người mua hàng.

---

# 2. KIẾN TRÚC BACKEND ADMIN

Admin Backend được tổ chức theo mô hình phân lớp:

Admin Panel (Frontend)
↓
Admin Router (API endpoints)
↓
Admin Service (Business Logic)
↓
Database

Trong project FastAPI, module Admin được đặt tại:

backend/Admin/

Cấu trúc:

backend/
└── Admin/
├── admin_router.py
├── admin_service.py
├── admin_schema.py
└── admin_auth.py

---

# 3. VAI TRÒ TỪNG FILE

## admin_router.py

Chứa các API endpoint của admin.

Ví dụ:

POST /admin/login  
GET /admin/products  
POST /admin/products

Router sẽ nhận request từ client và gọi service.

---

## admin_service.py

Chứa logic xử lý nghiệp vụ.

Ví dụ:

- tạo sản phẩm
- cập nhật sản phẩm
- xóa sản phẩm
- xử lý đơn hàng

Service là nơi làm việc trực tiếp với database.

---

## admin_schema.py

Chứa các schema dùng để validate dữ liệu request và response.

Ví dụ:

AdminLoginRequest  
ProductCreate  
ProductUpdate

Schema giúp đảm bảo dữ liệu gửi lên API đúng định dạng.

---

## admin_auth.py

Chứa logic xác thực admin.

Bao gồm:

- kiểm tra đăng nhập
- tạo JWT token
- verify token

---

# 4. CÁC CHỨC NĂNG ADMIN CẦN XÂY DỰNG

Admin Backend sẽ gồm các chức năng chính:

1. Xác thực Admin (Authentication)
2. Quản lý sản phẩm (Product Management)
3. Quản lý đơn hàng (Order Management)
4. Xem thông tin khách hàng (Customer Management)

---

# 5. THIẾT KẾ API DỰ KIẾN

## 5.1 Authentication

Đăng nhập admin.

POST /admin/login

Request:

{
"username": "admin",
"password": "123456"
}

Response:

{
"access_token": "...",
"token_type": "bearer"
}

---

## 5.2 Product Management

Lấy danh sách sản phẩm

GET /admin/products

---

Tạo sản phẩm mới

POST /admin/products

Request:

{
"name": "iPhone 15",
"price": 20000000,
"stock": 10,
"description": "Điện thoại Apple"
}

---

Cập nhật sản phẩm

PUT /admin/products/{product_id}

---

Xóa sản phẩm

DELETE /admin/products/{product_id}

---

## 5.3 Order Management

Lấy danh sách đơn hàng

GET /admin/orders

---

Xem chi tiết đơn hàng

GET /admin/orders/{order_id}

---

Cập nhật trạng thái đơn hàng

PATCH /admin/orders/{order_id}/status

Request:

{
"status": "shipped"
}

---

## 5.4 Customer Management

Xem danh sách khách hàng

GET /admin/customers

---

Xem chi tiết khách hàng

GET /admin/customers/{customer_id}

---

# 6. THỨ TỰ TRIỂN KHAI

Để phát triển module Admin Backend một cách ổn định, các bước sẽ được thực hiện theo thứ tự sau:

Bước 1: Xây dựng chức năng đăng nhập admin

Bước 2: Xây dựng API quản lý sản phẩm

Bước 3: Xây dựng API quản lý đơn hàng

Bước 4: Xây dựng API xem danh sách khách hàng

---

# 7. QUY TRÌNH PHÁT TRIỂN

Mỗi chức năng sẽ được thực hiện theo quy trình:

1. Thiết kế schema
2. Viết service xử lý logic
3. Tạo API router
4. Test API bằng Swagger (/docs)
5. Commit code lên branch feature/admin-backend

---

# 8. QUY TẮC COMMIT

Các commit message sẽ sử dụng tiếng Việt để dễ hiểu cho nhóm.

Ví dụ:

feat(admin): thêm API đăng nhập admin

feat(admin): thêm CRUD sản phẩm

feat(admin): thêm API quản lý đơn hàng

docs(admin): cập nhật kế hoạch admin backend

---

# 9. KẾT QUẢ MONG ĐỢI

Sau khi hoàn thành module Admin Backend, hệ thống sẽ cho phép:

- Admin đăng nhập vào hệ thống
- Admin quản lý sản phẩm
- Admin quản lý đơn hàng
- Admin xem thông tin khách hàng

Các API sẽ được tích hợp với Admin Panel frontend để quản trị hệ thống bán hàng.
