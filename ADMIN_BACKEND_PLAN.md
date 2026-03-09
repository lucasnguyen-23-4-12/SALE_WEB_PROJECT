# KẾ HOẠCH PHÁT TRIỂN BACKEND ADMIN

Project: SALE_WEB_PROJECT  
Phụ trách: Lê Huỳnh Tấn Đạt  
Module: Admin Backend

---

# 1. MỤC TIÊU MODULE ADMIN

Module Admin Backend được xây dựng nhằm cung cấp hệ thống API phục vụ cho trang quản trị (Admin Panel) của website bán hàng.

Admin có quyền thực hiện các thao tác quản trị hệ thống bao gồm:

- Quản lý sản phẩm
- Quản lý đơn hàng
- Xem thông tin khách hàng
- Kiểm soát hoạt động của hệ thống

Module này **chỉ phục vụ cho Admin Panel** và **không dùng cho người mua hàng (Customer)**.

Toàn bộ dữ liệu được lưu trữ trong **cùng một database chung của hệ thống**.

---

# 2. KIẾN TRÚC BACKEND ADMIN

Backend Admin được thiết kế theo mô hình **phân lớp (Layered Architecture)** nhằm đảm bảo:

- Dễ bảo trì
- Dễ mở rộng
- Tách biệt rõ logic hệ thống

Luồng xử lý:

Admin Panel (Frontend)  
↓  
Admin Router (API Endpoints)  
↓  
Admin Service (Business Logic)  
↓  
Database

Giải thích:

- **Frontend**: giao diện admin gửi request đến backend
- **Router**: định nghĩa các API endpoint
- **Service**: xử lý nghiệp vụ và tương tác với database
- **Database**: lưu trữ dữ liệu của hệ thống

---

# 3. CẤU TRÚC THƯ MỤC

Module Admin được đặt tại:

backend/Admin/

Cấu trúc:

backend/
└── Admin/
├── admin_router.py
├── admin_service.py
├── admin_schema.py
└── admin_auth.py

---

# 4. VAI TRÒ CỦA TỪNG FILE

## admin_router.py

Chứa các API endpoint của Admin.

Router sẽ nhận request từ client và chuyển đến Service để xử lý.

Ví dụ:

POST /admin/login  
GET /admin/products  
POST /admin/products

Router chỉ xử lý **routing và dependency**, không chứa logic nghiệp vụ.

---

## admin_service.py

Chứa logic xử lý nghiệp vụ của hệ thống.

Service sẽ tương tác trực tiếp với database.

Ví dụ:

- tạo sản phẩm
- cập nhật sản phẩm
- xóa sản phẩm
- lấy danh sách đơn hàng
- cập nhật trạng thái đơn hàng

Service giúp tách logic ra khỏi router để code dễ bảo trì.

---

## admin_schema.py

Chứa các schema dùng để validate dữ liệu request và response.

Sử dụng **Pydantic** để kiểm tra dữ liệu.

Ví dụ:

AdminLoginRequest  
ProductCreate  
ProductUpdate  
OrderStatusUpdate

Schema đảm bảo dữ liệu gửi lên API có đúng định dạng.

---

## admin_auth.py

Chứa logic xác thực Admin.

Bao gồm:

- kiểm tra đăng nhập
- tạo JWT token
- xác thực token
- bảo vệ các API quản trị

Admin API chỉ được truy cập khi token hợp lệ.

---

# 5. BẢO MẬT HỆ THỐNG ADMIN

Hệ thống sử dụng **JWT Authentication** để bảo vệ các API quản trị.

Quy trình xác thực:

Admin đăng nhập  
↓  
Server kiểm tra username và password  
↓  
Server tạo **JWT access token**  
↓  
Client gửi token trong header Authorization  
↓  
Server xác thực token trước khi cho phép truy cập API

Header request:

Authorization: Bearer <access_token>

Nếu token không hợp lệ hoặc không tồn tại:

Server trả về:

401 Unauthorized

---

# 6. CÁC CHỨC NĂNG ADMIN

Admin Backend bao gồm các chức năng chính:

1. Authentication (Xác thực admin)
2. Product Management (Quản lý sản phẩm)
3. Order Management (Quản lý đơn hàng)
4. Customer Management (Xem thông tin khách hàng)

---

# 7. THIẾT KẾ API

## 7.1 Authentication

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

## 7.2 Product Management

Lấy danh sách sản phẩm

GET /admin/products

Tạo sản phẩm mới

POST /admin/products

Request:

{
"name": "iPhone 15",
"price": 20000000,
"stock": 10,
"description": "Điện thoại Apple"
}

Cập nhật sản phẩm

PUT /admin/products/{product_id}

Xóa sản phẩm

DELETE /admin/products/{product_id}

---

## 7.3 Order Management

Lấy danh sách đơn hàng

GET /admin/orders

Xem chi tiết đơn hàng

GET /admin/orders/{order_id}

Cập nhật trạng thái đơn hàng

PATCH /admin/orders/{order_id}/status

Request:

{
"status": "shipped"
}

---

## 7.4 Customer Management

Xem danh sách khách hàng

GET /admin/customers

Xem chi tiết khách hàng

GET /admin/customers/{customer_id}

---

# 8. THỨ TỰ TRIỂN KHAI

Để đảm bảo hệ thống phát triển ổn định, module Admin Backend được triển khai theo thứ tự:

Bước 1: Xây dựng chức năng đăng nhập admin  
Bước 2: Xây dựng API quản lý sản phẩm  
Bước 3: Xây dựng API quản lý đơn hàng  
Bước 4: Xây dựng API xem danh sách khách hàng

---

# 9. QUY TRÌNH PHÁT TRIỂN

Mỗi chức năng sẽ được phát triển theo quy trình:

1. Thiết kế Schema
2. Viết Service xử lý logic
3. Tạo Router API
4. Test API bằng Swagger (/docs)
5. Commit code lên branch feature/admin-backend

---

# 10. QUY TẮC COMMIT

Các commit message sử dụng tiếng Việt để dễ hiểu cho nhóm.

Ví dụ:

feat(admin): thêm API đăng nhập admin

feat(admin): thêm CRUD sản phẩm

feat(admin): thêm API quản lý đơn hàng

docs(admin): cập nhật kế hoạch admin backend

---

# 11. KIỂM THỬ API

Toàn bộ API được kiểm thử bằng Swagger UI.

URL:

http://localhost:8000/docs

Các bước test:

1. Đăng nhập admin
2. Lấy JWT token
3. Authorize trong Swagger
4. Test các API quản trị

---

# 12. KẾT QUẢ MONG ĐỢI

Sau khi hoàn thành module Admin Backend, hệ thống sẽ cho phép:

- Admin đăng nhập vào hệ thống
- Admin quản lý sản phẩm
- Admin quản lý đơn hàng
- Admin xem thông tin khách hàng

Các API này sẽ được tích hợp với **Admin Panel Frontend** để tạo thành hệ thống quản trị hoàn chỉnh.
