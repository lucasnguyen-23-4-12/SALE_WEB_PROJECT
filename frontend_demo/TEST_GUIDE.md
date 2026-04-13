# Hướng dẫn test Web UI + kiểm tra DB

## 1) Chạy backend + frontend

### Backend
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger: `http://127.0.0.1:8000/docs`

### Frontend (port 5500)
```bash
cd frontend_demo
python -m http.server 5500
```

Mở: `http://127.0.0.1:5500/index.html`

## 2) Seed dữ liệu tối thiểu (Admin)
Customer không được tạo `products/categories/payment-methods`, nên DB cần có sẵn dữ liệu.

Trên Swagger:
1) `POST /admin/login` (form): username `admin`, password `admin123`
2) Authorize bằng token admin
3) Tạo:
   - `POST /categories/` (ít nhất 1 category)
   - `POST /products/` (ít nhất 1 product, dùng `category_id` vừa tạo)
   - `POST /payment-methods/` (ít nhất 1 payment method, ví dụ `{"mode_name":"COD"}`)

## 3) Test theo UI (Customer)

1) **Xem sản phẩm**
   - Vào `Sản phẩm` → thấy list từ backend
   - Click 1 sản phẩm → vào trang chi tiết

2) **Đăng ký / đăng nhập**
   - Vào `Tài khoản` → đăng ký (CustomerCreate)
   - Đăng nhập bằng email/sđt + password (CustomerLogin) → nhận JWT

3) **Wishlist**
   - Ở trang chi tiết sản phẩm → bấm `Yêu thích`
   - Vào `Tài khoản` → tab `Danh sách yêu thích` → thấy sản phẩm

4) **Review**
   - Ở trang chi tiết sản phẩm → gửi rating/comment
   - Review hiển thị lại trong danh sách reviews

5) **Giỏ hàng + Checkout + Order**
   - Thêm sản phẩm vào giỏ
   - Vào `Giỏ hàng` → `Tiến hành thanh toán`
   - Ở bước thanh toán, chọn `payment method` từ dropdown (được load từ DB)
   - Bấm `Đặt hàng ngay` → tạo `address` + `order`
   - Vào `Tài khoản` → tab `Đơn hàng của tôi` → thấy order mới

## 4) Kiểm tra DB (PostgreSQL)
Ví dụ bạn đã có `DATABASE_URL` trong `backend/.env`. Dưới đây là các câu lệnh psql phổ biến.

### Mở psql
```bash
psql "<DATABASE_URL>"
```

### Customers
```sql
SELECT "CustomerID","CustomerName","CustomerEmail","PhoneNumber","Address","CreatedAt"
FROM customers
ORDER BY "CustomerID"::int DESC
LIMIT 10;
```

### Categories / Products / PaymentMethods
```sql
SELECT "CategoryID","CategoryName" FROM categories ORDER BY "CategoryID"::int DESC LIMIT 10;
SELECT "ProductID","ProductName","Category","UnitPrice","StockQuantity" FROM products ORDER BY "ProductID"::int DESC LIMIT 10;
SELECT "PaymentMethodID","ModeName" FROM paymentmethods ORDER BY "PaymentMethodID"::int DESC LIMIT 10;
```

### Orders / OrderItems
```sql
SELECT "OrderID","CustomerID","PaymentMethodID","OrderDate","Status"
FROM orders
ORDER BY "OrderID"::int DESC
LIMIT 10;

SELECT "OrderItemID","OrderID","ProductID","Quantity","PriceAtPurchase","Amount"
FROM orderitems
ORDER BY "OrderItemID"::int DESC
LIMIT 20;
```

### Addresses / Wishlists / Reviews
```sql
SELECT "AddressID","CustomerID","Street","District","City","Zipcode","IsDefault"
FROM addresses
ORDER BY "AddressID"::int DESC
LIMIT 20;

SELECT "WishlistID","CustomerID","ProductID"
FROM wishlists
ORDER BY "WishlistID"::int DESC
LIMIT 20;

SELECT "ReviewID","ProductID","CustomerID","Rating","Comment","CreatedAt"
FROM reviews
ORDER BY "ReviewID"::int DESC
LIMIT 20;
```

