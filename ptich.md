# BẢN PHÁC THẢO PHÂN TÍCH VÀ THIẾT KẾ  
**Dự án:** Sale Web Project (Website bán hàng + API)  
**Môi trường hiện tại:** FastAPI + SQLAlchemy + PostgreSQL + Alembic, kèm frontend demo (HTML/CSS/JS thuần)

---

## 1. Giới thiệu & phạm vi

### 1.1. Mục tiêu
Dự án hướng đến xây dựng một hệ thống bán hàng trực tuyến quy mô nhỏ/ vừa, hỗ trợ hai nhóm người dùng:
- **Khách hàng (Customer):** xem sản phẩm, đăng ký/đăng nhập, quản lý thông tin cá nhân, tạo đơn hàng, quản lý địa chỉ, wishlist và đánh giá.
- **Quản trị viên (Admin):** đăng nhập quản trị, quản lý danh mục, sản phẩm, phương thức thanh toán và theo dõi/ xử lý đơn hàng.

Mục tiêu kỹ thuật của dự án là triển khai một API có cấu trúc rõ ràng (router → service → model), có xác thực JWT, có migration CSDL và có thể kết nối với giao diện web demo.

### 1.2. Phạm vi chức năng (scope)
Trong phạm vi hiện tại của project, hệ thống tập trung vào các nghiệp vụ cốt lõi:
- Quản lý **Customer / Product / Category / Order / Payment Method**
- Mở rộng thêm: **Review, Address, Wishlist**
- Phân quyền mức cơ bản: thao tác tạo/sửa/xóa các tài nguyên quản trị yêu cầu **Admin token**; các thao tác thuộc về khách hàng yêu cầu **Customer token** và kiểm tra “đúng chủ sở hữu dữ liệu”.

### 1.3. Các giả định/giới hạn
- Hệ thống hướng đến mục tiêu học tập và demo nên phần **Admin** hiện đang dùng tài khoản cố định (hard-code) để đăng nhập.
- Một số nghiệp vụ nâng cao (trừ tồn kho khi đặt hàng, thanh toán online, vận chuyển, mã giảm giá…) chưa triển khai đầy đủ và sẽ được đề xuất ở phần “Hướng phát triển”.

---

## 2. Phân tích yêu cầu

### 2.1. Tác nhân (Actors)
1) **Customer**
- Thực hiện các thao tác liên quan đến mua hàng và quản lý thông tin cá nhân.

2) **Admin**
- Quản trị dữ liệu nền tảng và theo dõi/ xử lý đơn hàng.

3) **Hệ thống (System)**
- Thực hiện xác thực, phân quyền, kiểm tra ràng buộc dữ liệu, ghi nhận và phản hồi kết quả.

### 2.2. Yêu cầu chức năng (Functional Requirements)

#### A. Nhóm chức năng khách hàng (Customer)
- **FR-C1:** Đăng ký tài khoản khách hàng.
- **FR-C2:** Đăng nhập bằng email hoặc số điện thoại, nhận **JWT access token**.
- **FR-C3:** Xem và cập nhật thông tin cá nhân (chỉ thao tác trên tài khoản của chính mình).
- **FR-C4:** Xem danh sách sản phẩm, xem chi tiết sản phẩm.
- **FR-C5:** Tạo đơn hàng gồm nhiều sản phẩm (order items) và theo dõi danh sách đơn của chính mình.
- **FR-C6:** Quản lý danh sách địa chỉ (thêm/xóa, xem theo khách hàng).
- **FR-C7:** Wishlist (thêm/xóa, xem theo khách hàng).
- **FR-C8:** Review sản phẩm (tạo review; xem review theo sản phẩm; xem review theo khách hàng).

#### B. Nhóm chức năng quản trị (Admin)
- **FR-A1:** Đăng nhập admin và nhận JWT token (bearer).
- **FR-A2:** Quản lý danh mục (tạo/sửa/xóa; khách hàng chỉ được xem).
- **FR-A3:** Quản lý sản phẩm (tạo/sửa/xóa; khách hàng chỉ được xem).
- **FR-A4:** Quản lý phương thức thanh toán (tạo/sửa/xóa; khách hàng được xem để checkout).
- **FR-A5:** Xem danh sách đơn hàng, xem chi tiết đơn; cập nhật trạng thái đơn hàng.

#### C. Nhóm chức năng hệ thống
- **FR-S1:** Phân trang danh sách (skip/limit) cho các endpoint liệt kê.
- **FR-S2:** Ràng buộc dữ liệu (khóa ngoại, unique email, kiểm tra tồn tại danh mục khi tạo sản phẩm…).
- **FR-S3:** Trả về mã lỗi HTTP và thông báo phù hợp khi sai dữ liệu hoặc thiếu quyền.

### 2.3. Yêu cầu phi chức năng (Non-functional Requirements)
- **NFR-1 (Bảo mật):** mật khẩu khách hàng được băm; API bảo vệ bằng JWT; dữ liệu riêng tư chỉ truy cập đúng chủ.
- **NFR-2 (Tính đúng đắn):** đảm bảo ràng buộc khóa ngoại, không tạo order rỗng, quantity > 0.
- **NFR-3 (Khả năng mở rộng):** cấu trúc phân lớp (router/service/model) giúp dễ phát triển thêm nghiệp vụ.
- **NFR-4 (Khả năng bảo trì):** tách riêng schema (Pydantic) và model (SQLAlchemy) để kiểm soát dữ liệu vào/ra.
- **NFR-5 (Tính tương thích):** backend mở CORS để frontend demo (port 5500) gọi API trực tiếp.

### 2.4. Quy tắc nghiệp vụ (Business Rules) tổng quát
- **BR-1:** Email khách hàng là duy nhất.
- **BR-2:** Khách hàng chỉ xem/sửa/xóa dữ liệu “thuộc về mình” (customer_id trong token phải trùng dữ liệu thao tác).
- **BR-3:** Chỉ admin mới được tạo/sửa/xóa product/category/payment method.
- **BR-4:** Đơn hàng phải có ít nhất 1 item; số lượng item > 0; sản phẩm phải tồn tại.

---

## 3. Thiết kế kiến trúc hệ thống

### 3.1. Mô hình kiến trúc tổng thể
Hệ thống được tổ chức theo mô hình 3 tầng:

```
Trình duyệt (Frontend demo HTML/JS)
        |
        |  HTTP (JSON + Bearer Token)
        v
FastAPI Backend (Routers / Services / Schemas)
        |
        |  SQLAlchemy ORM
        v
PostgreSQL Database (Alembic migrations)
```

Ý nghĩa:
- **Frontend demo** chỉ đóng vai trò giao diện, gọi API trực tiếp qua `fetch`.
- **Backend** chịu trách nhiệm nghiệp vụ, bảo mật, validate dữ liệu, truy cập CSDL.
- **Database** lưu dữ liệu và ràng buộc khóa ngoại/ chỉ mục.

### 3.2. Thiết kế phân lớp trong Backend
Backend được tổ chức theo các thư mục chính:
- `backend/app/models/`: định nghĩa ORM models (Customer, Product, Order, …)
- `backend/app/schemas/`: định nghĩa Pydantic schemas (Create/Update/Response)
- `backend/app/services/`: xử lý nghiệp vụ, truy vấn CSDL, raise exception
- `backend/app/routers/`: định tuyến API (FastAPI APIRouter), gọi service và gắn dependency auth
- `backend/app/core/`: dependency `get_db`, auth cho customer, cấu hình logging (nếu mở rộng)
- `backend/Admin/`: nhóm chức năng admin (auth + router + service)

Mối quan hệ gọi:
`Router → Service → (Model/DB Session) → Response Schema`

### 3.3. Thiết kế xác thực & phân quyền (JWT)
Hệ thống dùng JWT với thuật toán HS256.

1) **Customer token**
- Nhận token qua `POST /customers/login` hoặc `POST /customers/token` (OAuth2 form).
- Token chứa các thông tin: `sub = customer_id`, `role = "customer"`, `exp`.
- Khi gọi các API protected, frontend gửi header:
  - `Authorization: Bearer <token>`

2) **Admin token**
- Nhận token qua `POST /admin/login` (OAuth2 form).
- Token dùng `sub = "admin"`; phía backend kiểm tra token hợp lệ và đúng admin.

3) **Kiểm soát quyền truy cập**
- Các endpoint tạo/sửa/xóa product/category/payment method bắt buộc `Depends(get_current_admin)`.
- Các endpoint thao tác dữ liệu khách hàng bắt buộc `Depends(get_current_customer)` và đối chiếu `customer_id`.

### 3.4. Thiết kế xử lý lỗi
Các service sử dụng nhóm exception chuẩn hóa (HTTPException) để trả về:
- `404 Not Found`: tài nguyên không tồn tại
- `409 Conflict`: dữ liệu đã tồn tại (ví dụ email)
- `400 Bad Request`: lỗi nghiệp vụ (order rỗng, quantity <= 0, lỗi transaction)
- `401 Unauthorized`: sai mật khẩu hoặc chưa xác thực
- `403 Forbidden`: truy cập sai chủ sở hữu

---

## 4. Thiết kế cơ sở dữ liệu (CSDL)

### 4.1. Tổng quan mô hình dữ liệu (ERD mô tả)
Các thực thể chính và quan hệ:
- `Category (1) — (N) Product`
- `Customer (1) — (N) Order`
- `Order (1) — (N) OrderItem`
- `Product (1) — (N) OrderItem`
- `PaymentMethod (1) — (N) Order`
- `Customer (1) — (N) Address`
- `Customer (1) — (N) Review` và `Product (1) — (N) Review`
- `Customer (1) — (N) Wishlist` và `Product (1) — (N) Wishlist`

### 4.2. Quy ước khóa & kiểu dữ liệu ID
- Các khóa chính/ khóa ngoại trong CSDL hiện được lưu dạng **VARCHAR(50)**.
- ID vẫn có thể được sinh theo cơ chế sequence của PostgreSQL nhưng được ép kiểu sang text (`nextval(...)::text`), giúp thống nhất kiểu dữ liệu và thuận tiện khi tích hợp phía frontend.

### 4.3. Danh sách bảng chính (tóm tắt)

#### 1) `customers`
- **PK:** `CustomerID` (varchar)
- Thuộc tính chính: `CustomerName`, `CustomerEmail` (unique), `PhoneNumber`, `Password_Hash`, `Address`, `CreatedAt`, `UpdatedAt`, `IsActive`

#### 2) `categories`
- **PK:** `CategoryID` (varchar)
- Thuộc tính: `CategoryName`, `Subcategory`

#### 3) `products`
- **PK:** `ProductID` (varchar)
- **FK:** `Category` → `categories.CategoryID`
- Thuộc tính: `ProductName`, `Description`, `Image_url`, `UnitPrice`, `DiscountPercent`, `StockQuantity`, `RatingAvg`, `TotalReviews`

#### 4) `paymentmethods`
- **PK:** `PaymentMethodID` (varchar)
- Thuộc tính: `ModeName`, `PayDate`

#### 5) `orders`
- **PK:** `OrderID` (varchar)
- **FK:** `CustomerID` → `customers.CustomerID`
- **FK:** `PaymentMethodID` → `paymentmethods.PaymentMethodID`
- Thuộc tính: `OrderDate`, `Status`, `ShippingAddress`, `ShippingFee`, `DiscountAmount`

#### 6) `orderitems`
- **PK:** `OrderItemID` (varchar)
- **FK:** `OrderID` → `orders.OrderID`
- **FK:** `ProductID` → `products.ProductID`
- Thuộc tính: `Quantity`, `Amount`, `PriceAtPurchase`, `Profit`, `Discount`

#### 7) `addresses`
- **PK:** `AddressID` (varchar)
- **FK:** `CustomerID` → `customers.CustomerID`
- Thuộc tính: `Street`, `City`, `District`, `Zipcode`, `IsDefault`

#### 8) `reviews`
- **PK:** `ReviewID` (varchar)
- **FK:** `ProductID` → `products.ProductID`
- **FK:** `CustomerID` → `customers.CustomerID`
- Thuộc tính: `Rating`, `Comment`, `CreatedAt`

#### 9) `wishlists`
- **PK:** `WishlistID` (varchar)
- **FK:** `CustomerID` → `customers.CustomerID`
- **FK:** `ProductID` → `products.ProductID`

### 4.4. Chỉ mục & tối ưu truy vấn (mức cơ bản)
Hệ thống có các index cho:
- Các cột ID chính (PK) và các cột FK thường truy vấn (`CustomerID`, `ProductID`, `OrderID`, …)
- Cột `CustomerEmail` có index unique để phục vụ đăng nhập/đăng ký.

---

## 5. Thiết kế API (RESTful)

### 5.1. Quy ước chung
- Dữ liệu trao đổi theo JSON.
- Các danh sách hỗ trợ phân trang: `skip` và `limit`.
- Các endpoint cần đăng nhập gửi kèm header `Authorization: Bearer <token>`.

### 5.2. Nhóm endpoint chính (tóm tắt theo module)

#### A. Customers (`/customers`)
- `POST /customers/`: đăng ký
- `POST /customers/login`: đăng nhập (JSON)
- `POST /customers/token`: đăng nhập (OAuth2 form)
- `GET /customers/`: danh sách (Admin-only)
- `GET /customers/{customer_id}`: xem chi tiết (Customer-only, đúng chủ)
- `PUT /customers/{customer_id}`: cập nhật (Customer-only, đúng chủ)
- `DELETE /customers/{customer_id}`: xóa (Customer-only, đúng chủ)

#### B. Categories (`/categories`)
- `GET /categories/`: danh sách
- `GET /categories/{category_id}`: chi tiết
- `POST /categories/`: tạo (Admin-only)
- `PUT /categories/{category_id}`: sửa (Admin-only)
- `DELETE /categories/{category_id}`: xóa (Admin-only)

#### C. Products (`/products`)
- `GET /products/`: danh sách
- `GET /products/{product_id}`: chi tiết
- `POST /products/`: tạo (Admin-only)
- `PUT /products/{product_id}`: sửa (Admin-only)
- `DELETE /products/{product_id}`: xóa (Admin-only)

#### D. Payment Methods (`/payment-methods`)
- `GET /payment-methods/`: danh sách
- `GET /payment-methods/{payment_method_id}`: chi tiết
- `POST /payment-methods/`: tạo (Admin-only)
- `PUT /payment-methods/{payment_method_id}`: sửa (Admin-only)
- `DELETE /payment-methods/{payment_method_id}`: xóa (Admin-only)

#### E. Orders (`/orders`)
- `POST /orders/`: tạo order (Customer-only, customer_id phải trùng token)
- `GET /orders/`: danh sách order của chính mình (Customer-only)
- `GET /orders/{order_id}`: chi tiết (Customer-only, đúng chủ)
- `DELETE /orders/{order_id}`: xóa (Customer-only, đúng chủ)

#### F. Addresses (`/addresses`)
- `POST /addresses/`: tạo địa chỉ (Customer-only, đúng chủ)
- `GET /addresses/customer/{customer_id}`: danh sách địa chỉ (Customer-only, đúng chủ)
- `DELETE /addresses/{address_id}`: xóa địa chỉ (Customer-only, đúng chủ)

#### G. Wishlists (`/wishlists`)
- `POST /wishlists/`: thêm wishlist (Customer-only, đúng chủ)
- `GET /wishlists/customer/{customer_id}`: xem wishlist (Customer-only, đúng chủ)
- `DELETE /wishlists/{wishlist_id}`: xóa wishlist (Customer-only, đúng chủ)

#### H. Reviews (`/reviews`)
- `POST /reviews/`: tạo review (Customer-only, đúng chủ)
- `GET /reviews/product/{product_id}`: xem review theo sản phẩm (public)
- `GET /reviews/customer/{customer_id}`: xem review theo khách hàng (Customer-only, đúng chủ)

#### I. Admin (`/admin`)
- `POST /admin/login`: đăng nhập admin (OAuth2 form)
- `GET /admin/products`: danh sách sản phẩm (Admin-only)
- `GET /admin/products/{product_id}`: chi tiết sản phẩm (Admin-only)
- `POST /admin/products`: tạo sản phẩm (Admin-only)
- `PUT /admin/products/{product_id}`: sửa sản phẩm (Admin-only)
- `DELETE /admin/products/{product_id}`: xóa sản phẩm (Admin-only)
- `GET /admin/orders`: danh sách đơn (Admin-only)
- `GET /admin/orders/{order_id}`: chi tiết đơn (Admin-only)
- `PATCH /admin/orders/{order_id}/status`: cập nhật trạng thái (Admin-only)

### 5.3. Gợi ý trạng thái đơn hàng (tham khảo)
Trạng thái đang được lưu dạng chuỗi (`Status`) và có thể chuẩn hóa theo bộ giá trị:
- `Pending` → `Confirmed` → `Shipping` → `Completed`
- Trường hợp đặc biệt: `Canceled`, `Failed`

---

## 6. Phác thảo luồng nghiệp vụ chính

### 6.1. Luồng đăng ký & đăng nhập khách hàng
1) Customer gửi thông tin đăng ký → API tạo customer và lưu mật khẩu dạng hash.  
2) Customer đăng nhập bằng email/phone + password → API trả JWT token.  
3) Frontend lưu token và dùng để gọi các API yêu cầu xác thực.

### 6.2. Luồng mua hàng (tạo đơn)
Luồng tổng quát:
1) Customer xem danh sách sản phẩm và thêm vào giỏ hàng (frontend demo lưu giỏ hàng bằng LocalStorage).  
2) Customer chọn phương thức thanh toán, nhập địa chỉ giao hàng.  
3) Frontend gửi `POST /orders/` gồm `customer_id`, `payment_method_id`, `items[]`.  
4) Backend kiểm tra:
   - customer_id trùng với `sub` trong token
   - payment method tồn tại
   - items không rỗng, quantity hợp lệ
   - product tồn tại
5) Backend tạo `orders` và `orderitems`, commit transaction.

Ghi chú: hiện tại luồng này chưa trừ tồn kho; phần này có thể bổ sung ở mục phát triển.

### 6.3. Luồng quản trị (admin)
1) Admin đăng nhập tại `POST /admin/login` (username/password).  
2) Dùng token để:
   - Tạo danh mục, sản phẩm, payment method
   - Xem danh sách đơn và cập nhật trạng thái đơn

---

## 7. Phác thảo thiết kế giao diện (Frontend demo)

### 7.1. Công nghệ
- HTML/CSS/JavaScript thuần, không dùng framework.
- Gọi API bằng `fetch`, tự gắn `Authorization` header khi cần.

### 7.2. Các màn hình chính (tham khảo theo thư mục `frontend_demo/`)
- `index.html`: trang chủ / nổi bật
- `products.html`: danh sách sản phẩm
- `product-detail.html`: chi tiết sản phẩm + wishlist + review
- `cart.html`: giỏ hàng (LocalStorage)
- `checkout.html`: thanh toán (tạo order)
- `customer-login.html`: đăng ký/đăng nhập, lưu token

### 7.3. Lưu trữ phía trình duyệt (LocalStorage)
Frontend demo sử dụng các key chính:
- `customer_token`: lưu JWT của customer
- `user_profile`: cache thông tin người dùng
- `cart`: giỏ hàng
- `api_base`: base URL backend (mặc định `http://127.0.0.1:8000`)

---

## 8. Hướng phát triển (đề xuất)
Để hoàn thiện hệ thống theo hướng “gần thực tế” hơn, có thể bổ sung:
1) **Quản lý admin bằng bảng CSDL** (thay vì hard-code), hỗ trợ nhiều admin và phân quyền theo vai trò.  
2) **Trừ tồn kho khi tạo order** + cơ chế kiểm tra số lượng tồn.  
3) **Tính tổng tiền chuẩn hóa** (tổng order, phí ship, giảm giá) và lưu trường tổng vào bảng orders.  
4) **Thanh toán online** (mô phỏng) + trạng thái thanh toán; tích hợp cổng thanh toán (mức demo).  
5) **Chuẩn hóa trạng thái** bằng enum/constant và rule chuyển trạng thái.  
6) **Báo cáo thống kê**: doanh thu theo ngày/tháng, top sản phẩm, tỉ lệ hủy đơn.  
7) **Kiểm thử**: mở rộng test cho nghiệp vụ checkout và phân quyền.

---

## 9. Kết luận
Bản phác thảo trên mô tả tổng quan phân tích yêu cầu và thiết kế hệ thống của Sale Web Project dựa trên cấu trúc project hiện tại. Hệ thống đã có các thành phần chính: API theo mô hình phân lớp, xác thực JWT, CSDL PostgreSQL với migration, và frontend demo có thể gọi API để minh họa luồng nghiệp vụ. Đây là nền tảng phù hợp để tiếp tục mở rộng các chức năng nâng cao trong giai đoạn tiếp theo.

