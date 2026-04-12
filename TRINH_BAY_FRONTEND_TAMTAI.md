# TAI LIEU TRINH BAY FRONTEND - WEB TAM TAI

Cap nhat: 2026-04-12  
Pham vi: Frontend la trong tam, co lien ket voi tong quan Backend + Database de de trinh bay end-to-end.

---

## 1) Tong quan he thong (noi mo dau 30-60 giay)

He thong Web TAM TAI gom 3 phan:

- `Frontend`: giao dien nguoi dung va giao dien admin.
- `Backend`: FastAPI xu ly nghiep vu, xac thuc, API.
- `Database`: PostgreSQL luu du lieu san pham, user, don hang, review, ma giam gia.

Luong ket noi:

1. User thao tac tren giao dien HTML.
2. JavaScript frontend goi API den `http://127.0.0.1:8000`.
3. Backend xu ly logic va doc/ghi PostgreSQL.
4. Backend tra JSON, frontend render lai giao dien.

> Ghi chu thuyet trinh: Nhan manh frontend khong tu tao du lieu, frontend dang lay du lieu that tu backend.

---

## 2) Cay thu muc Frontend (hien trang thuc te)

```text
frontend/
  html/
    core/
      landing.html
    products/
      products.html
      product-detail.html
    cart/
      cart.html
      checkout.html
      all-orders.html
      order-detail.html
    auth/
      login.html
      register.html
      forgot-password.html
    user/
      profile.html
      address.html
      password.html
      product-reviews.html
      notification.html
    admin/
      admin.html

  js/
    core/
      common.js
      landing.js
    products/
      products.js
      product-detail.js
    cart/
      cart.js
      checkout.js
      all-orders.js
      order-detail.js
      orders-data.js
    auth/
      login.js
      register.js
      forgot-password.js
    user/
      profile.js
      address.js
      password.js
      product-reviews.js
      notification.js
    admin/
      admin.js

  css/
    core/
      landing.css
    products/
      products.css
      product-detail.css
    cart/
      cart.css
      checkout.css
      all-orders.css
      order-detail.css
    auth/
      login.css
      register.css
    user/
      profile.css
      notification.css
    admin/
      admin.css

  images/
    ... (logo, anh san pham, etc.)
```

> Ghi chu thuyet trinh:
> - Trang chu hien tai la `frontend/html/core/landing.html`.
> - `frontend/html/core/index.html` da duoc xoa.
> - Da don cac file legacy khong con duoc include de tranh roi logic.

---

## 3) Mapping trang -> chuc nang -> file JS/CSS -> API

## 3.1 Khu vuc Core

### `frontend/html/core/landing.html`

- Muc dich: trang vao dau tien, hero, category noi bat, dieu huong vao san pham/tai khoan.
- JS: `frontend/js/core/common.js`, `frontend/js/core/landing.js`
- CSS: `frontend/css/core/landing.css`
- API su dung:
  - `GET /categories?skip=0&limit=100`
  - `GET /products?skip=0&limit=500`
- Hanh vi:
  - Render so lieu tong quan (so san pham, danh muc, rating, review).
  - Hero slider theo san pham noi bat.
  - Click category -> sang `products.html?category=...`
  - Nut tai khoan: neu da login thi vao profile, chua login thi vao login.

> Ghi chu thuyet trinh: Day la trang de "khoi dong hanh trinh mua hang", khong phai trang dat hang truc tiep.

---

## 3.2 Khu vuc Products

### `frontend/html/products/products.html`

- Muc dich: hien danh sach san pham.
- JS: `frontend/js/products/products.js` + `common.js`
- CSS: `frontend/css/products/products.css`
- API:
  - `GET /categories?skip=0&limit=100`
  - `GET /products?skip=0&limit=100`
- Hanh vi:
  - Tim kiem, loc theo danh muc, loc theo gia, sap xep.
  - Click card -> trang chi tiet.
  - `Them vao gio` -> cap nhat localStorage.
  - `Mua ngay` -> vao checkout.

### `frontend/html/products/product-detail.html`

- Muc dich: hien chi tiet 1 san pham.
- JS: `frontend/js/products/product-detail.js` + `common.js`
- CSS: `frontend/css/products/product-detail.css`
- API:
  - `GET /products/{id}`
  - `GET /categories/{id}` (de hien nhan category)
- Hanh vi:
  - Cho chon so luong.
  - Them vao gio / mua ngay.

> Ghi chu thuyet trinh: Cum Products la diem trung tam tao conversion (xem -> them gio -> mua).

---

## 3.3 Khu vuc Cart + Checkout + Order

### `frontend/html/cart/cart.html`

- Muc dich: gio hang.
- JS: `frontend/js/cart/cart.js` + `common.js`
- CSS: `frontend/css/cart/cart.css`
- API:
  - `GET /products/{id}`
  - `GET /products?skip=0&limit=100` (goi y san pham lien quan)
- Hanh vi:
  - Dong bo lai thong tin sp (gia/hinh/ton kho).
  - Tang/giam/xoa so luong.
  - Tinh tong tien.

### `frontend/html/cart/checkout.html`

- Muc dich: dat hang.
- JS: `frontend/js/cart/checkout.js` + `common.js`
- CSS: `frontend/css/cart/checkout.css`
- API:
  - `GET /customers/me` (can token)
  - `GET /payment-methods?skip=0&limit=100`
  - `POST /orders/` (can token)
- Hanh vi:
  - Neu chua login -> chuyen login.
  - Tao don hang.
  - Thanh cong -> dieu huong sang `order-detail` hoac `all-orders`.

### `frontend/html/cart/all-orders.html`

- Muc dich: danh sach don cua user.
- JS: `frontend/js/cart/all-orders.js`, `frontend/js/cart/orders-data.js`, `common.js`
- CSS: `frontend/css/cart/all-orders.css`
- API:
  - `GET /orders?skip=0&limit=100` (can token)

### `frontend/html/cart/order-detail.html`

- Muc dich: chi tiet 1 don.
- JS: `frontend/js/cart/order-detail.js`, `frontend/js/cart/orders-data.js`, `common.js`
- CSS: `frontend/css/cart/order-detail.css`
- API:
  - `GET /orders/{order_id}` (can token)

> Ghi chu thuyet trinh: Cum Cart/Checkout da noi den order that tren DB, khong phai mock.

---

## 3.4 Khu vuc Auth

### `frontend/html/auth/login.html`

- Muc dich: dang nhap user/admin.
- JS: `frontend/js/auth/login.js` + `common.js`
- CSS: `frontend/css/auth/login.css`
- API:
  - `POST /customers/login`
  - `POST /admin/login`
  - `POST /customers/google`
- Hanh vi:
  - Luu `access_token`, `token_type`, `tamtai_role` vao localStorage.
  - Dieu huong theo role (`user` hoac `admin`).

### `frontend/html/auth/register.html`

- Muc dich: dang ky user.
- JS: `frontend/js/auth/register.js` + `common.js`
- CSS: `frontend/css/auth/register.css`
- API:
  - `POST /customers/register/request-otp`
  - `POST /customers/register/with-otp`
  - `POST /customers/google`

### `frontend/html/auth/forgot-password.html`

- Muc dich: quen mat khau qua OTP email.
- JS: `frontend/js/auth/forgot-password.js` + `common.js`
- CSS: `frontend/css/auth/login.css`
- API:
  - `POST /customers/forgot-password/request-otp`
  - `POST /customers/forgot-password/verify-otp`
  - `POST /customers/forgot-password/reset`

> Ghi chu thuyet trinh: Auth hien tai da co login user, login admin, OTP reset, va Google login.

---

## 3.5 Khu vuc User

### `frontend/html/user/profile.html`

- Muc dich: ho so user + thong tin don gan day.
- JS: `frontend/js/user/profile.js` + `common.js`
- CSS: `frontend/css/user/profile.css`
- API:
  - `GET /customers/me`
  - `PUT /customers/{customer_id}`
  - `GET /orders?skip=0&limit=20`

### `frontend/html/user/address.html`

- Muc dich: quan ly dia chi giao hang.
- JS: `frontend/js/user/address.js` + `common.js`
- CSS: `frontend/css/user/profile.css`
- API:
  - `GET /customers/me`
  - `GET /addresses/customer/{customer_id}`
  - `POST /addresses/`
  - `DELETE /addresses/{address_id}`

### `frontend/html/user/password.html`

- Muc dich: doi mat khau.
- JS: `frontend/js/user/password.js` + `common.js`
- CSS: `frontend/css/user/profile.css`
- API:
  - `GET /customers/me`
  - `POST /customers/change-password`

### `frontend/html/user/product-reviews.html`

- Muc dich: viet/quan ly danh gia cua user.
- JS: `frontend/js/user/product-reviews.js` + `common.js`
- CSS: `frontend/css/user/profile.css`
- API:
  - `GET /customers/me`
  - `GET /products?skip=0&limit=100`
  - `GET /reviews/customer/{customer_id}`
  - `POST /reviews/`

### `frontend/html/user/notification.html`

- Muc dich: xem thong bao.
- JS: `frontend/js/user/notification.js` + `common.js`
- CSS: `frontend/css/user/notification.css`
- API: chua goi API backend (dang xu ly tren UI local).

> Ghi chu thuyet trinh: User module da bao phu profile, dia chi, mat khau, review, don hang.

---

## 3.6 Khu vuc Admin

### `frontend/html/admin/admin.html`

- Muc dich: dashboard quan tri tong hop.
- JS: `frontend/js/admin/admin.js` + `common.js`
- CSS: `frontend/css/admin/admin.css`
- API:
  - `GET /admin/me`
  - `GET /admin/dashboard`
  - `GET /admin/products`, `POST /admin/products`, `PUT /admin/products/{id}`, `DELETE /admin/products/{id}`
  - `GET /admin/orders`, `PATCH /admin/orders/{id}/status`
  - `GET /admin/customers`, `PATCH /admin/customers/{id}`
  - `GET /admin/discount-codes`, `POST /admin/discount-codes`, `PATCH /admin/discount-codes/{id}`, `DELETE /admin/discount-codes/{id}`
  - `GET /categories?skip=0&limit=100` (de phuc vu form san pham)

> Ghi chu thuyet trinh: Day la dashboard that, da thao tac truc tiep tren du lieu backend/database.

---

## 4) File trung tam cua Frontend: `common.js`

File: `frontend/js/core/common.js`

Vai tro:

- Dinh nghia `API_BASE_URL = http://127.0.0.1:8000`.
- Cung cap helper:
  - `buildApiUrl()`
  - `fetchJson()`
  - `formatCurrency()`
  - `setupSearchRedirect()`
  - `logout()`
- Quan ly gio hang tach theo user:
  - `tamtai_cart` cho guest
  - `tamtai_cart_user_<customer_id>` cho user login
- Quan ly profile/session qua localStorage.

LocalStorage keys quan trong:

- `access_token`
- `token_type`
- `tamtai_role` (`guest`, `user`, `admin`)
- `tamtai_customer_id`
- `tamtai_customer_profile`
- `tamtai_profile`
- `tamtai_cart_user_<customer_id>`

> Ghi chu thuyet trinh: Neu can tom gon frontend trong 1 cau, co the noi "common.js la xuong song cua frontend".

---

## 5) Cong nghe dang dung o Frontend

- `HTML` cho cau truc trang.
- `CSS` cho giao dien (chia module theo `core/products/cart/auth/user/admin`).
- `JavaScript thuan` (Vanilla JS), khong dung React/Vue.
- `fetch API` de goi backend.
- `localStorage` de giu session, role, cart, profile.
- `JWT Bearer token` cho endpoint can dang nhap.
- `Google Identity Services` (dang nhap Google o login/register).
- `Font Awesome` cho icon.
- `Google Fonts` (`Anton`, `Be Vietnam Pro`, co trang dung them `JetBrains Mono`).

> Ghi chu thuyet trinh: Kien truc nay de hoc/bao ve de an rat ro rang, de debug vi khong co framework phuc tap.

---

## 6) Luong nghiep vu can demo khi trinh bay

## 6.1 Luong mua hang co login

1. Vao `landing.html`.
2. Mo `products.html`, loc + tim san pham.
3. Vao `product-detail.html`.
4. Them gio / mua ngay.
5. Vao `cart.html`.
6. Dat hang tai `checkout.html`.
7. Mo `all-orders.html` va `order-detail.html` de chung minh don da tao.

## 6.2 Luong user account

1. Dang ky/Dang nhap.
2. Vao profile sua thong tin.
3. Quan ly dia chi.
4. Doi mat khau.
5. Viet review san pham.

## 6.3 Luong admin

1. Login admin.
2. Vao dashboard admin.
3. CRUD product.
4. Cap nhat trang thai don.
5. Khoa/mo user.
6. Tao/sua/xoa ma giam gia.

> Ghi chu thuyet trinh: 3 luong tren la xuyen suot toan bo frontend hien tai.

---

## 7) Diem dang hoat dong tot

- Frontend da noi du lieu that voi backend cho cac luong chinh.
- San pham, chi tiet, gio hang, checkout, profile, admin da hoat dong theo API.
- Role `user/admin` da duoc tach ro rang.
- Gio hang da tach theo tung user.
- Admin dashboard da co nghiep vu quan tri thuc te.

---

## 8) Diem can luu y khi bao ve/deploy

- `notification.html` hien tai chu yeu la UI local, chua dong bo API thong bao.
- Frontend la web tinh, nen state dang dua nhieu vao localStorage.
- Nen co them buoc don tai lieu cu co nhac den `index.html` (vi file nay da xoa).

> Ghi chu thuyet trinh: Nhan manh day la "backlog ky thuat", khong phai loi nghiep vu chinh.

---

## 9) Script noi nhanh (2-3 phut)

Ban co the doc gan nhu nguyen van:

1. "Frontend TAM TAI duoc xay dung bang HTML/CSS/JavaScript thuan, khong dung framework."
2. "Trang vao la landing, tu do dieu huong sang danh sach san pham, chi tiet, gio hang va checkout."
3. "Toan bo du lieu duoc lay that tu backend FastAPI qua fetch API, khong mock."
4. "common.js la file trung tam de quan ly API URL, session JWT, localStorage va gio hang theo tung user."
5. "User co day du luong dang ky, dang nhap, profile, dia chi, doi mat khau, review, lich su don."
6. "Admin co dashboard va CRUD thuc te cho san pham, don hang, user va ma giam gia."
7. "He thong da co du luong de demo end-to-end tu xem hang den dat hang va quan tri."

---

## 10) Ket luan 1 cau

Frontend hien tai da dat muc tieu "web ban hang full flow": co giao dien user + admin, co ket noi API that, co dat hang that, va co kha nang demo end-to-end ro rang.
