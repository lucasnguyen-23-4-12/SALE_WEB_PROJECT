# Hướng Dẫn Lưu Thông Tin Khách Hàng (End-to-End)

## 1. Mục tiêu tài liệu
Tài liệu này tổng hợp toàn bộ phần đã làm để:
- Đăng ký/đăng nhập lưu đúng khách hàng.
- Đồng bộ dữ liệu khách hàng lên trang Profile/Địa chỉ/Mật khẩu/Đánh giá.
- Quên mật khẩu bằng OTP email và cập nhật mật khẩu thật trong database.
- Google login dùng đúng tài khoản theo email đã tồn tại.

Phạm vi tập trung: luồng dữ liệu khách hàng (customer data lifecycle).

---

## 2. Kiến trúc tổng quan

### Backend
- `FastAPI` + `SQLAlchemy` + `PostgreSQL`
- Auth bằng JWT bearer token.
- OTP email dùng SMTP (Gmail App Password).

### Frontend
- HTML/CSS/JS thuần.
- Lưu phiên đăng nhập bằng `localStorage` (`access_token`, `tamtai_role`, `tamtai_customer_id`, `tamtai_profile`).
- Dữ liệu chính luôn lấy từ backend qua API.

---

## 3. Thiết lập database PostgreSQL từ đầu

## 3.1 Tạo database
Trong pgAdmin:
1. Chuột phải `Databases` -> `Create` -> `Database...`
2. Name: `sale_web_db`
3. Owner: user postgres hoặc user bạn đang dùng
4. Save

## 3.2 Cấu hình `.env` backend
File: `backend/.env`

Các biến quan trọng:
```env
DATABASE_URL=postgresql://sale_web_user:Saleweb123@localhost:5432/sale_web_db
SECRET_KEY=your_secret_key_here
GOOGLE_CLIENT_ID=27435447565-fk6hsgmd17rqjuqegeqvq1monbo632gr.apps.googleusercontent.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_FROM_EMAIL=your_gmail@gmail.com
SMTP_USE_TLS=true
EMAIL_OTP_TTL_MINUTES=10
EMAIL_OTP_MAX_ATTEMPTS=5
EMAIL_OTP_RESEND_COOLDOWN_SECONDS=60
```

## 3.3 Tạo bảng
Trong thư mục `backend`:
```bash
pip install -r requirements.txt
alembic upgrade head
```

Kiểm tra nhanh bảng:
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public'
ORDER BY table_name;
```

Các bảng liên quan khách hàng cần có:
- `customers`
- `addresses`
- `orders`
- `reviews`

---

## 4. Bản đồ file đã chỉnh và chức năng chính

## 4.1 Backend (dữ liệu + API)
- `backend/app/routers/customer_router.py`
  - Auth thường: `/customers/login`
  - Auth Google: `/customers/google`
  - Profile: `/customers/me`
  - Đổi mật khẩu khi đã đăng nhập: `/customers/change-password`
  - Quên mật khẩu:
    - `/customers/forgot-password/request-otp`
    - `/customers/forgot-password/verify-otp`
    - `/customers/forgot-password/reset`
  - Đăng ký OTP:
    - `/customers/register/request-otp`
    - `/customers/register/with-otp`

- `backend/app/services/customer_service.py`
  - Xác thực user/password.
  - Google: nếu email đã tồn tại -> dùng lại user cũ; email mới -> tạo user mới.
  - Đổi mật khẩu theo phiên đăng nhập (`change_customer_password`).
  - Reset mật khẩu theo email (`reset_customer_password_by_email`).

- `backend/app/services/email_otp_service.py`
  - Gửi OTP email.
  - Verify OTP.
  - Sinh `reset_token` cho luồng quên mật khẩu.
  - Consume `reset_token` (chỉ dùng 1 lần, có TTL).

- `backend/app/routers/address_router.py`
  - CRUD địa chỉ theo `customer_id` + token user.

- `backend/app/routers/review_router.py`
  - Tạo/lấy đánh giá theo customer/product.

- `backend/app/services/review_service.py`
  - Upsert review theo cặp `(product_id, customer_id)`:
    - Chưa có -> tạo mới
    - Có rồi -> cập nhật review cũ

## 4.2 Frontend (đồng bộ profile khách hàng)
- `frontend/js/core/common.js`
  - Cấu hình `API_BASE_URL`, `GOOGLE_CLIENT_ID`.
  - `getProfile/saveProfile`.
  - `logout` + xóa session localStorage.

- `frontend/js/auth/login.js`
  - Login thường (`/customers/login`) + Google (`/customers/google`).
  - Lưu token và role.

- `frontend/js/auth/register.js`
  - Gửi OTP đăng ký (`/customers/register/request-otp`).
  - Đăng ký xác thực OTP (`/customers/register/with-otp`).

- `frontend/js/auth/forgot-password.js`
  - Quên mật khẩu 3 bước:
    1. Gửi OTP
    2. Verify OTP
    3. Reset password

- `frontend/js/user/profile.js`
  - Lấy profile từ `/customers/me`.
  - Lấy đơn hàng từ `/orders`.
  - Thiếu dữ liệu thì hiển thị `chưa có`.

- `frontend/js/user/address.js`
  - Lấy profile từ `/customers/me`.
  - Lấy/thêm/xóa địa chỉ:
    - `GET /addresses/customer/{customer_id}`
    - `POST /addresses/`
    - `DELETE /addresses/{address_id}`

- `frontend/js/user/password.js`
  - Sidebar đồng bộ theo user đang login.
  - Đổi mật khẩu thật qua `POST /customers/change-password`.

- `frontend/js/user/product-reviews.js`
  - Lấy review của user hiện tại.
  - Gửi/cập nhật review vào DB qua `POST /reviews/`.

- `frontend/html/user/*.html`
  - Sidebar + logout + khu vực hiển thị dữ liệu profile.

---

## 5. Luồng hoạt động chi tiết

## 5.1 Đăng ký thường bằng email + OTP
1. Người dùng nhập email -> bấm gửi OTP.
2. Frontend gọi `POST /customers/register/request-otp`.
3. Backend gửi OTP qua SMTP.
4. Người dùng nhập OTP + mật khẩu -> gửi form.
5. Frontend gọi `POST /customers/register/with-otp`.
6. Backend verify OTP, tạo `customer` trong DB.

## 5.2 Đăng nhập thường
1. Frontend gọi `POST /customers/login`.
2. Backend kiểm tra email/phone + password hash.
3. Trả JWT token.
4. Frontend lưu token vào localStorage.

## 5.3 Đăng nhập/đăng ký Google
1. Frontend lấy `id_token` từ Google SDK.
2. Gọi `POST /customers/google`.
3. Backend verify token bằng `GOOGLE_CLIENT_ID`.
4. Nếu email đã tồn tại -> dùng user cũ.
5. Nếu email chưa tồn tại -> tạo user mới (tên mặc định theo phần trước `@`).

## 5.4 Vào trang profile/address/password/reviews
1. Frontend đọc token trong localStorage.
2. Gọi `GET /customers/me`.
3. Đổ dữ liệu vào sidebar/form.
4. Field trống -> hiển thị `chưa có`.

## 5.5 Quên mật khẩu
1. Nhập email -> `POST /customers/forgot-password/request-otp`
2. Nhập OTP -> `POST /customers/forgot-password/verify-otp` -> nhận `reset_token`
3. Nhập mật khẩu mới -> `POST /customers/forgot-password/reset`
4. Backend cập nhật `password_hash` trong bảng `customers`.

## 5.6 Đổi mật khẩu trong trang user/password
1. User đang login nhập mật khẩu hiện tại + mật khẩu mới.
2. Frontend gọi `POST /customers/change-password` với bearer token.
3. Backend:
   - check mật khẩu hiện tại
   - check độ mạnh mật khẩu mới
   - hash và lưu DB
4. Frontend logout để user đăng nhập lại bằng mật khẩu mới.

---

## 6. Cách kiểm tra nhanh sau khi sửa

1. Chạy backend:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

2. Mở frontend và `Ctrl + F5`.

3. Test checklist:
- Đăng ký OTP tạo được user mới trong `customers`.
- Login đúng user, vào profile thấy đúng email.
- Sửa địa chỉ lưu vào `addresses`.
- Đổi mật khẩu xong đăng nhập lại bằng mật khẩu mới.
- Quên mật khẩu (OTP) reset được pass.
- Gửi đánh giá xong reload trang vẫn thấy review.

---

## 7. SQL kiểm tra dữ liệu khách hàng

## 7.1 Thông tin customer theo email
```sql
SELECT
  "CustomerID",
  "CustomerName",
  "CustomerEmail",
  "PhoneNumber",
  "Address",
  "CreatedAt",
  "UpdatedAt"
FROM customers
WHERE lower("CustomerEmail") = lower('your_email@gmail.com');
```

## 7.2 Địa chỉ của customer
```sql
SELECT
  a."AddressID",
  a."Street",
  a."District",
  a."City",
  a."Zipcode",
  a."IsDefault"
FROM addresses a
JOIN customers c ON c."CustomerID" = a."CustomerID"
WHERE lower(c."CustomerEmail") = lower('your_email@gmail.com')
ORDER BY a."IsDefault" DESC, a."AddressID" DESC;
```

## 7.3 Đánh giá của customer
```sql
SELECT
  r."ReviewID",
  r."ProductID",
  r."Rating",
  r."Comment",
  r."CreatedAt"
FROM reviews r
JOIN customers c ON c."CustomerID" = r."CustomerID"
WHERE lower(c."CustomerEmail") = lower('your_email@gmail.com')
ORDER BY r."CreatedAt" DESC;
```

---

## 8. Lỗi thường gặp và cách xử lý
- Google login lỗi `Invalid Google token`
  - Nguyên nhân: lệch `GOOGLE_CLIENT_ID` giữa frontend và backend.
  - Cách xử lý: đồng bộ cùng 1 Client ID.

- OTP không gửi được
  - Kiểm tra `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` (App Password 16 ký tự), TLS.

- Đổi mật khẩu báo thành công nhưng không login được
  - Đảm bảo backend đã restart và frontend gọi đúng `POST /customers/change-password`.

- Trang hiển thị dữ liệu cũ
  - `Ctrl + F5`.
  - Kiểm tra token localStorage có đúng user hiện tại không.

---

## 9. Ghi chú bảo mật
- Không commit `.env` thật lên git.
- Đổi `SECRET_KEY` sang chuỗi mạnh.
- Đổi mật khẩu DB và App Password định kỳ.
