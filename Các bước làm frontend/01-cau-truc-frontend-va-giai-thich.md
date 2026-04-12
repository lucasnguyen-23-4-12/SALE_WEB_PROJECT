# Cấu Trúc Frontend Và Giải Thích File

## 1) Cấu trúc hiện tại

```text
frontend/
├── html/
│   ├── core/
│   │   ├── index.html
│   │   └── landing.html
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── forgot-password.html
│   ├── user/
│   │   ├── profile.html
│   │   └── notification.html
│   ├── products/
│   │   ├── products.html
│   │   └── product-detail.html
│   ├── cart/
│   │   ├── cart.html
│   │   └── checkout.html
│   └── admin/
│       └── admin.html
├── css/
│   ├── core/
│   │   ├── home.css
│   │   └── landing.css
│   ├── auth/
│   │   ├── login.css
│   │   └── register.css
│   ├── user/
│   │   ├── profile.css
│   │   └── notification.css
│   ├── products/
│   │   ├── products.css
│   │   └── product-detail.css
│   ├── cart/
│   │   ├── cart.css
│   │   └── checkout.css
│   └── admin/
│       └── admin.css
├── js/
│   ├── core/
│   │   └── home.js
│   ├── auth/
│   │   └── customer.js
│   ├── products/
│   │   ├── products.js
│   │   └── product-detail.js
│   └── cart/
│       ├── cart.js
│       └── checkout.js
├── images/
│   ├── modern-logo-with-gradient-squares.png
│   └── acer-refurbished-laptop-500x500.webp
└── FRONTEND_BACKEND_PLAN.md
```

## 2) Ý nghĩa từng nhóm thư mục

- `frontend/html/`: Chứa các trang giao diện theo chức năng.
- `frontend/css/`: Mỗi trang có file CSS tương ứng theo cùng nhóm chức năng.
- `frontend/js/`: Logic client-side cho từng nhóm trang.
- `frontend/images/`: Ảnh dùng chung toàn frontend.

## 3) Giải thích nhanh từng trang HTML

- `html/core/index.html`: Trang chính/home.
- `html/core/landing.html`: Landing page giới thiệu.
- `html/auth/login.html`: Trang đăng nhập (email/password, Google sign-in).
- `html/auth/register.html`: Trang đăng ký (OTP email, Google sign-up).
- `html/auth/forgot-password.html`: Trang quên mật khẩu.
- `html/user/profile.html`: Hồ sơ người dùng.
- `html/user/notification.html`: Thông báo người dùng.
- `html/products/products.html`: Danh sách sản phẩm.
- `html/products/product-detail.html`: Chi tiết sản phẩm.
- `html/cart/cart.html`: Giỏ hàng.
- `html/cart/checkout.html`: Thanh toán.
- `html/admin/admin.html`: Trang quản trị.

## 4) Quy tắc mapping file (rất quan trọng)

- 1 trang HTML nên map 1 file CSS cùng chức năng.
- Link CSS/JS trong HTML đang dùng đường dẫn tương đối theo cấu trúc mới.
- Khi thêm trang mới, nên thêm đúng cả 3 lớp:
  - `html/<nhom>/<page>.html`
  - `css/<nhom>/<page>.css`
  - `js/<nhom>/<page>.js`

## 5) Ví dụ thêm trang mới

Ví dụ thêm trang "order-history":

- Tạo `frontend/html/user/order-history.html`
- Tạo `frontend/css/user/order-history.css`
- Tạo `frontend/js/user/order-history.js`
- Trong HTML, link:

```html
<link rel="stylesheet" href="../../css/user/order-history.css">
<script defer src="../../js/user/order-history.js"></script>
```
