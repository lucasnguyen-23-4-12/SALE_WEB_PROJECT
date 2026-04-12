# TAI LIEU TONG QUAN WEB TAM TAI

## 1. Muc tieu cua he thong

Day la web ban hang cong nghe gom 3 phan chinh:

- `Frontend`: giao dien nguoi dung va giao dien admin.
- `Backend`: API xu ly nghiep vu, xac thuc, truy van du lieu, quan tri.
- `Database`: PostgreSQL luu san pham, nguoi dung, don hang, danh muc, review, ma giam gia...

Web hien tai cho phep:

- Xem danh sach san pham.
- Xem chi tiet san pham.
- Dang ky, dang nhap, quen mat khau.
- Them vao gio hang, dat hang, xem lich su don hang.
- Quan ly thong tin user.
- Quan tri admin: san pham, don hang, user, ma giam gia.

## 2. Cau truc tong quan

### Thu muc lon

- `frontend/`: HTML, CSS, JavaScript cho giao dien.
- `backend/`: FastAPI, SQLAlchemy, Alembic, model, router, service.
- `project_seed_data/`: du lieu goc da duoc xu ly de nhap database.

### Cach 3 phan noi voi nhau

1. Nguoi dung thao tac tren trang HTML.
2. JavaScript trong `frontend/js` goi API den backend o `http://127.0.0.1:8000`.
3. Backend xu ly logic va doc/ghi du lieu trong PostgreSQL.
4. Ket qua tra ve JSON de frontend render len giao dien.

## 3. Frontend

## 3.1 Cong nghe

Frontend hien tai la web tinh:

- `HTML`
- `CSS`
- `JavaScript thuan`

Khong dung React/Vue. Toan bo logic nam trong cac file `.js`.

## 3.2 Cau truc frontend

### Trang giao dien chinh

- `frontend/html/core/landing.html`
- `frontend/html/products/products.html`
- `frontend/html/products/product-detail.html`
- `frontend/html/cart/cart.html`
- `frontend/html/cart/checkout.html`
- `frontend/html/cart/all-orders.html`
- `frontend/html/cart/order-detail.html`
- `frontend/html/auth/login.html`
- `frontend/html/auth/register.html`
- `frontend/html/auth/forgot-password.html`
- `frontend/html/user/profile.html`
- `frontend/html/user/address.html`
- `frontend/html/user/password.html`
- `frontend/html/user/product-reviews.html`
- `frontend/html/user/notification.html`
- `frontend/html/admin/admin.html`

### JavaScript chuc nang

- `frontend/js/core/common.js`: file dung chung quan trong nhat.
- `frontend/js/core/landing.js`: logic landing page.
- `frontend/js/products/products.js`: danh sach san pham, loc, sap xep.
- `frontend/js/products/product-detail.js`: trang chi tiet san pham.
- `frontend/js/cart/cart.js`: gio hang.
- `frontend/js/cart/checkout.js`: dat hang.
- `frontend/js/cart/all-orders.js`: danh sach don cua user.
- `frontend/js/cart/order-detail.js`: chi tiet don.
- `frontend/js/auth/login.js`: dang nhap user va admin.
- `frontend/js/auth/register.js`: dang ky user.
- `frontend/js/auth/forgot-password.js`: quen mat khau.
- `frontend/js/user/profile.js`: ho so user.
- `frontend/js/user/address.js`: dia chi user.
- `frontend/js/user/password.js`: doi mat khau.
- `frontend/js/admin/admin.js`: dashboard admin moi da noi vao database that.

## 3.3 File dung chung `common.js`

File `frontend/js/core/common.js` dong vai tro trung tam cho frontend:

- Chua `API_BASE_URL`.
- Quan ly `localStorage`.
- Quan ly gio hang theo tung user.
- Chua cac ham format tien, build URL API, fetch JSON.
- Quan ly session va logout.

### Cac key localStorage quan trong

- `access_token`: token dang nhap.
- `token_type`
- `tamtai_role`: `guest`, `user`, `admin`.
- `tamtai_customer_id`
- `tamtai_customer_profile`
- `tamtai_profile`
- `tamtai_cart_user_<customer_id>`: gio hang rieng tung user.

## 3.4 Luong hoat dong frontend

### A. Trang landing

- Hien banner, danh muc noi bat, huong dieu huong vao san pham.
- Neu da dang nhap thi nut tai khoan dua den profile.
- Neu la admin thi co the vao trang admin.

### B. Trang san pham

- Lay du lieu tu API `/products`.
- Render danh sach san pham that tu database.
- Ho tro tim kiem, loc theo category, loc theo gia, sap xep.

### C. Trang chi tiet san pham

- Lay san pham theo `id` tren URL.
- Hien thong tin, gia, ton kho, danh gia.
- Nut `Them vao gio` dua san pham vao gio hang trong `localStorage`.
- Nut `Mua ngay` dua user vao luong thanh toan.

### D. Gio hang

- Hien cac san pham da them.
- Dong bo lai thong tin san pham voi API de tranh gia/hinh cu.
- Cho phep tang, giam, xoa san pham.
- De xuat them san pham lien quan.

### E. Checkout

- Lay gio hang cua user dang dang nhap.
- Lay thong tin customer hien tai.
- Tao don hang bang API `/orders`.
- Sau khi dat thanh cong thi cap nhat database va tru ton kho.

### F. Profile user

- Lay thong tin `/customers/me`.
- Cho phep sua profile.
- Xem lich su don hang.
- Doi mat khau.

### G. Trang admin

Trang `frontend/html/admin/admin.html` hien tai da la dashboard that:

- Tong quan du lieu he thong.
- Danh sach san pham that.
- Them, sua, xoa san pham.
- Danh sach don hang that va cap nhat trang thai.
- Danh sach user that va khoa/mo tai khoan.
- Tao, sua, bat/tat, xoa ma giam gia.

## 3.5 Cach frontend goi backend

Frontend goi backend bang `fetch`.

Vi du:

- `GET /products`
- `GET /products/{id}`
- `POST /customers/login`
- `POST /orders`
- `GET /admin/dashboard`

Neu endpoint can dang nhap:

- Frontend gui `Authorization: Bearer <token>`

## 4. Backend

## 4.1 Cong nghe

Backend dung:

- `FastAPI`
- `SQLAlchemy`
- `Alembic`
- `PostgreSQL`
- `JWT`

## 4.2 Diem vao chinh

File chinh:

- `backend/app/main.py`

File nay:

- Tao app FastAPI.
- Cau hinh CORS cho frontend.
- Dang ky router.
- Xu ly logging JSON.
- Xu ly loi chung.

## 4.3 Kieu to chuc backend

Backend duoc tach theo 3 lop:

- `models`: dinh nghia bang database.
- `schemas`: dinh nghia request/response.
- `services`: xu ly nghiep vu.
- `routers`: dinh nghia API endpoint.

## 4.4 Router hien co

### Customer

Folder:

- `backend/app/routers/customer_router.py`

Chuc nang:

- Dang ky user.
- Dang nhap user.
- Google login.
- Quen mat khau qua OTP email.
- Lay profile user.
- Sua profile.
- Doi mat khau.
- Admin xem danh sach customer qua router customer va qua admin router.

### Product

- `backend/app/routers/product_router.py`

Chuc nang:

- Lay danh sach san pham.
- Lay chi tiet san pham.
- Tao, sua, xoa san pham neu la admin.

### Order

- `backend/app/routers/order_router.py`

Chuc nang:

- Tao don hang.
- Lay danh sach don cua user hien tai.
- Lay chi tiet don.
- Xoa don cua chinh user neu duoc phep.

### Category

- `backend/app/routers/category_router.py`

Chuc nang:

- Lay danh sach category.
- Lay category theo id.
- Tao, sua, xoa category neu la admin.

### Payment

- `backend/app/routers/payment_router.py`

Chuc nang:

- Quan ly phuong thuc thanh toan.

### Review

- `backend/app/routers/review_router.py`

Chuc nang:

- Quan ly danh gia san pham.

### Address

- `backend/app/routers/address_router.py`

Chuc nang:

- Quan ly dia chi giao hang.

### Wishlist

- `backend/app/routers/wishlist_router.py`

Chuc nang:

- Quan ly san pham yeu thich.

### Admin

- `backend/Admin/admin_router.py`

Chuc nang:

- Dang nhap admin.
- Dashboard tong quan.
- Lay san pham cho admin.
- CRUD san pham.
- Lay va cap nhat don hang.
- Lay va cap nhat user.
- Tao/sua/xoa ma giam gia.

## 4.5 Authentication

### Customer auth

File:

- `backend/app/core/customer_auth.py`

Chuc nang:

- Tao JWT cho customer.
- Doc token de lay current customer.

### Admin auth

File:

- `backend/Admin/admin_auth.py`

Chuc nang:

- Xac thuc admin theo `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
- Tao JWT cho admin.
- Bao ve route admin bang Bearer token.

## 4.6 Service layer

Moi nghiep vu chinh co service rieng:

- `product_service.py`
- `order_service.py`
- `customer_service.py`
- `category_service.py`
- `review_service.py`
- `address_service.py`
- `wishlist_service.py`
- `payment_service.py`
- `Admin/admin_service.py`

Service layer la noi xu ly logic that, vi du:

- Kiem tra category co ton tai truoc khi tao product.
- Tao order va tru ton kho.
- Hash password.
- Validate email.
- Tong hop thong ke admin.

## 4.7 Logging va xu ly loi

Trong `backend/app/main.py` co:

- Middleware log request.
- Gan `request_id`.
- JSON error payload.
- Handler cho `HTTPException`, `ValidationError`, loi chung.

Muc dich:

- De debug de hon.
- De frontend nhan thong diep loi ro rang hon.

## 4.8 Luong backend quan trong

### A. Dang nhap customer

1. Frontend gui email/sdt + password.
2. Backend tim customer trong bang `customers`.
3. Kiem tra password hash.
4. Tao JWT.
5. Frontend luu token vao `localStorage`.

### B. Dat hang

1. Frontend gui `customer_id`, `payment_method_id`, `items`.
2. Backend kiem tra customer ton tai.
3. Kiem tra payment method ton tai.
4. Kiem tra tung product.
5. Kiem tra ton kho.
6. Tao `orders`.
7. Tao `orderitems`.
8. Tru `stock_quantity`.

### C. Admin xem dashboard

1. Frontend goi `/admin/dashboard`.
2. Backend tong hop:
   - so san pham
   - so user
   - so don
   - doanh thu
   - san pham sap het hang
   - ma giam gia dang hoat dong
3. Tra ve mot JSON tong hop.

### D. Admin tao ma giam gia

1. Admin nhap code, phan tram giam, product, customer.
2. Backend validate product/customer neu co chon.
3. Luu vao bang `discountcodes`.

## 5. Database

## 5.1 Cong nghe va ket noi

Database dung `PostgreSQL`.

Ket noi nam o:

- `backend/app/config.py`
- `backend/app/database.py`

Bien moi truong quan trong:

- `DATABASE_URL`

## 5.2 ORM model

Model dang duoc load trong:

- `backend/app/models/__init__.py`

Hien tai co cac bang chinh:

- `customers`
- `products`
- `categories`
- `orders`
- `orderitems`
- `paymentmethods`
- `reviews`
- `addresses`
- `wishlists`
- `discountcodes`

## 5.3 Mo ta tung bang

### `categories`

Luu danh muc san pham.

Cot chinh:

- `CategoryID`
- `CategoryName`
- `Subcategory`

### `products`

Luu san pham.

Cot chinh:

- `ProductID`
- `Category`
- `ProductName`
- `Description`
- `Image_url`
- `UnitPrice`
- `DiscountPercent`
- `StockQuantity`
- `RatingAvg`
- `TotalReviews`

Quan he:

- 1 category co nhieu products.
- 1 product co the nam trong nhieu orderitems.
- 1 product co nhieu reviews.
- 1 product co nhieu discount codes.

### `customers`

Luu tai khoan nguoi dung.

Cot chinh:

- `CustomerID`
- `CustomerName`
- `CustomerEmail`
- `PhoneNumber`
- `Password_Hash`
- `Address`
- `CreatedAt`
- `UpdatedAt`
- `IsActive`

Quan he:

- 1 customer co nhieu orders.
- 1 customer co nhieu reviews.
- 1 customer co nhieu addresses.
- 1 customer co nhieu wishlist items.
- 1 customer co nhieu discount codes duoc gan rieng.

### `orders`

Luu thong tin don hang tong.

Cot chinh:

- `OrderID`
- `CustomerID`
- `PaymentMethodID`
- `OrderDate`
- `Status`
- `ShippingAddress`
- `ShippingFee`
- `DiscountAmount`

### `orderitems`

Luu tung dong san pham trong don.

Cot chinh:

- `OrderItemID`
- `OrderID`
- `ProductID`
- `Quantity`
- `Amount`
- `PriceAtPurchase`
- `Profit`
- `Discount`

### `paymentmethods`

Luu phuong thuc thanh toan.

### `reviews`

Luu danh gia san pham cua customer.

### `addresses`

Luu dia chi giao hang cua customer.

### `wishlists`

Luu san pham yeu thich.

### `discountcodes`

Bang moi da them cho admin.

Cot chinh:

- `DiscountCodeID`
- `Code`
- `Description`
- `DiscountPercent`
- `ProductID`
- `CustomerID`
- `UsageLimit`
- `UsedCount`
- `StartsAt`
- `ExpiresAt`
- `IsActive`
- `CreatedAt`

Y nghia:

- Co the tao ma giam gia chung.
- Hoac gan cho 1 san pham cu the.
- Hoac gan cho 1 user cu the.

## 5.4 Migration

Migration duoc quan ly bang Alembic:

- `backend/alembic/versions/`

Alembic dung de:

- Tao bang moi.
- Them cot moi.
- Sua kieu du lieu.
- Dong bo schema giua code va database.

Migration moi nhat da them:

- bang `discountcodes`

## 5.5 Luong du lieu trong database

### Khi tao don hang

- `customers` -> xac dinh ai mua.
- `orders` -> tao don tong.
- `orderitems` -> them tung san pham.
- `products` -> tru ton kho.

### Khi admin quan ly san pham

- doc/ghi truc tiep bang `products`
- tham chieu `categories`

### Khi admin quan ly user

- doc/ghi bang `customers`

### Khi admin tao ma giam gia

- doc/ghi bang `discountcodes`
- co the tham chieu `products` va `customers`

## 6. Cac luong van hanh quan trong cua web

## 6.1 Khach vao xem hang

1. Mo landing page.
2. Chuyen sang trang san pham.
3. Frontend goi API lay product tu backend.
4. Backend doc `products` + `categories`.
5. Frontend render danh sach.

## 6.2 Khach dang nhap

1. Gui thong tin den backend.
2. Backend tra JWT.
3. Frontend luu token va role.
4. Cac trang sau dung token nay de goi API can dang nhap.

## 6.3 Khach them gio hang

1. Bam `Them vao gio`.
2. Frontend luu vao gio hang rieng trong `localStorage`.
3. Khi mo gio hang, frontend goi lai API product de cap nhat gia/hinh ton kho moi.

## 6.4 Khach dat hang

1. Tu trang checkout gui du lieu order.
2. Backend tao order.
3. Database ghi `orders` va `orderitems`.
4. Stock san pham giam.

## 6.5 Admin quan tri

1. Dang nhap admin.
2. Vao `admin.html`.
3. Frontend goi `/admin/dashboard`.
4. Admin co the chuyen tab:
   - tong quan
   - san pham
   - don hang
   - user
   - ma giam gia

## 7. Diem dang hoat dong tot

- Frontend da noi du lieu that cho danh sach san pham, chi tiet san pham, gio hang, checkout, profile, admin.
- Backend dang doc/ghi truc tiep PostgreSQL.
- Admin da co dashboard va CRUD thuc te.
- Gio hang da tach theo tung user.

## 8. Diem can luu y

- Ma giam gia hien da co bang va admin CRUD, nhung neu muon ap ma ngay trong checkout thi can noi tiep vao luong dat hang.
- Trong database hien tai co the van con mot so ban ghi test cu, admin se hien dung theo du lieu that dang co.
- Frontend van la web tinh, nen nhieu state duoc quan ly o localStorage va bang JavaScript thuong.

## 9. File nen doc neu muon hieu nhanh

Neu muon nam nhanh toan bo he thong, uu tien doc theo thu tu:

1. `backend/app/main.py`
2. `backend/app/models/__init__.py`
3. `backend/app/routers/product_router.py`
4. `backend/app/routers/customer_router.py`
5. `backend/app/routers/order_router.py`
6. `backend/Admin/admin_router.py`
7. `backend/Admin/admin_service.py`
8. `frontend/js/core/common.js`
9. `frontend/js/products/products.js`
10. `frontend/js/products/product-detail.js`
11. `frontend/js/cart/cart.js`
12. `frontend/js/cart/checkout.js`
13. `frontend/js/admin/admin.js`

## 10. Tom tat ngan gon

Web nay la mo hinh:

- `Frontend HTML/CSS/JS` de hien thi va gui request.
- `Backend FastAPI` de xu ly logic.
- `PostgreSQL` de luu du lieu.

Frontend khong tu tao du lieu, ma se lay du lieu tu backend.
Backend khong luu tam bang file, ma luu vao database.
Admin da co the quan tri du lieu that ngay tren giao dien.

