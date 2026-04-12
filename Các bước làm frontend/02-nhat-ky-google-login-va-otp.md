# Nhật Ký Làm Google Login/Register + OTP Mail (Chi Tiết Dễ Hiểu)

Phạm vi tài liệu này chỉ tính phần đã làm từ lúc triển khai:
- Đăng nhập/đăng ký bằng Google
- Gửi mã OTP email 6 số (hạn 10 phút) cho đăng ký

---

## A) Mục tiêu

1. Nút Google ở `login.html` và `register.html` phải dùng thật, không còn demo.
2. Đăng ký thường phải có OTP email 6 số, nhập đúng mới tạo tài khoản.
3. OTP hết hạn sau 10 phút.

---

## B) Những gì đã làm cho Google Login/Register

### B1. Backend

Đã thêm endpoint:
- `POST /customers/google`

Luồng xử lý:
1. Frontend nhận `id_token` từ Google GIS.
2. Gửi lên backend `POST /customers/google`.
3. Backend verify token bằng `google-auth` + `GOOGLE_CLIENT_ID`.
4. Lấy `email`, `name` từ token.
5. Nếu user chưa có thì tạo mới, nếu có rồi thì dùng lại.
6. Trả JWT nội bộ (`access_token`) cho frontend.

File chính đã chỉnh:
- `backend/app/routers/customer_router.py`
- `backend/app/services/customer_service.py`
- `backend/app/schemas/auth.py`
- `backend/app/config.py`
- `backend/requirements.txt`
- `backend/.env`

### B2. Frontend

Đã cập nhật cả 2 trang:
- `frontend/html/auth/login.html`
- `frontend/html/auth/register.html`

Nội dung đã làm:
1. Nhúng script Google GIS:
   - `https://accounts.google.com/gsi/client`
2. Render nút Google bằng `google.accounts.id.renderButton(...)`.
3. Callback nhận `response.credential`.
4. Gọi API backend `/customers/google`.
5. Lưu `access_token` vào `localStorage`.
6. Redirect về `profile.html` khi thành công.

---

## C) Những gì đã làm cho OTP Email 6 số

### C1. Backend API OTP

Đã thêm 2 endpoint mới:
- `POST /customers/register/request-otp`
- `POST /customers/register/with-otp`

Ý nghĩa:
1. `request-otp`: nhận email, tạo OTP 6 số, gửi qua mail.
2. `with-otp`: verify OTP + tạo tài khoản nếu OTP hợp lệ.

### C2. Logic OTP

Đã tạo service OTP riêng:
- `backend/app/services/email_otp_service.py`

Logic chính:
1. Tạo mã random 6 chữ số.
2. Không lưu plain text OTP, lưu hash SHA-256.
3. TTL mặc định 10 phút.
4. Cooldown resend mặc định 60 giây.
5. Max sai OTP mặc định 5 lần.
6. Verify đúng thì consume mã (xóa mã ngay sau khi dùng).

### C3. Form đăng ký frontend

Trang đã cập nhật:
- `frontend/html/auth/register.html`

UI/logic đã thêm:
1. Input OTP 6 số.
2. Nút `Send code` gọi API `request-otp`.
3. Hiển thị trạng thái gửi mã + đếm ngược resend.
4. Submit form sẽ gọi `register/with-otp`.
5. Chỉ đăng ký thành công khi OTP đúng.

CSS đã thêm:
- `frontend/css/auth/register.css`

---

## D) Cấu hình môi trường cần có

Trong `backend/.env` cần các biến:

```env
GOOGLE_CLIENT_ID=...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_USE_TLS=true
EMAIL_OTP_TTL_MINUTES=10
EMAIL_OTP_MAX_ATTEMPTS=5
EMAIL_OTP_RESEND_COOLDOWN_SECONDS=60
```

Lưu ý quan trọng:
- `SMTP_HOST` phải là hostname server SMTP (`smtp.gmail.com`), không phải email.
- `SMTP_PASSWORD` là Google App Password, không phải mật khẩu Gmail thường.

---

## E) Cách test end-to-end

1. Chạy backend.
2. Mở `frontend/html/auth/register.html`.
3. Nhập email, bấm `Send code`.
4. Kiểm tra mail nhận OTP.
5. Nhập OTP + mật khẩu + xác nhận.
6. Bấm đăng ký.
7. Nếu thành công, chuyển qua `login.html`.
8. Đăng nhập lại bằng email/password để xác nhận tài khoản đã tạo.
9. Test thêm Google sign-in/sign-up ở cả login/register.

---

## F) Ghi chú kỹ thuật

- OTP hiện lưu trong memory tiến trình backend.
- Nếu restart backend, OTP cũ sẽ mất (đúng theo cơ chế in-memory).
- Nếu cần production chuẩn hơn, nên lưu OTP vào Redis/DB với TTL.
