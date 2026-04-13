# Tech Store Frontend Demo (Kết nối Backend)

Frontend demo (HTML/CSS/JS thuần) kết nối trực tiếp với FastAPI backend trong `backend/`.

## Chạy dự án

### 1) Backend (FastAPI)
Từ root repo:

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger: `http://127.0.0.1:8000/docs`

### 2) Frontend (khuyến nghị port 5500)
Backend đã allow CORS cho `http://127.0.0.1:5500`/`http://localhost:5500`.

**Cách A (VS Code Live Server):**
- Mở `frontend_demo/index.html` → “Open with Live Server” (port 5500).

**Cách B (Python http.server port 5500):**
```bash
cd frontend_demo
python -m http.server 5500
```

Mở: `http://127.0.0.1:5500/index.html`

## Tính năng customer (UI)
- Xem danh sách sản phẩm, chi tiết sản phẩm
- Giỏ hàng (LocalStorage)
- Đăng ký / đăng nhập (JWT)
- Wishlist (DB)
- Reviews (DB)
- Addresses (DB)
- Tạo order + xem lịch sử order (DB)

## Lưu ý
- `POST/PUT/DELETE` cho `products/categories/payment-methods` là **Admin-only** (customer chỉ đọc).
- Checkout cần DB có **ít nhất 1 payment method** (ví dụ `COD`). Nếu chưa có, admin tạo qua Swagger `/payment-methods/` (đăng nhập `/admin/login`).

## Cấu hình API base
Mặc định frontend gọi backend tại `http://127.0.0.1:8000`. Nếu bạn đổi host/port, cập nhật trong `frontend_demo/js/app.js` hoặc set `localStorage.api_base`.

