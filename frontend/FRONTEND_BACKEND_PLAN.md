# FRONTEND BACKEND PLAN

## 1. Tổng quan backend

Backend là một API FastAPI chạy trên `http://localhost:8000`.

Các nhóm chức năng chính:
- Khách hàng (Customer)
- Sản phẩm (Product)
- Danh mục (Category)
- Giỏ hàng / Đơn hàng (Order)
- Địa chỉ (Address)
- Danh sách yêu thích (Wishlist)
- Đánh giá (Review)
- Phương thức thanh toán (Payment Method)
- Quản trị viên (Admin)

## 2. Cấu trúc router và endpoint chính

### 2.1 Product
- `GET /products/` - lấy danh sách sản phẩm
- `GET /products/{product_id}` - lấy chi tiết sản phẩm
- `POST /products/` - tạo sản phẩm (admin)
- `PUT /products/{product_id}` - cập nhật sản phẩm (admin)
- `DELETE /products/{product_id}` - xóa sản phẩm (admin)

### 2.2 Category
- `GET /categories/` - lấy danh sách danh mục
- `GET /categories/{category_id}` - lấy chi tiết danh mục
- `POST /categories/` - tạo danh mục (admin)
- `PUT /categories/{category_id}` - cập nhật danh mục (admin)
- `DELETE /categories/{category_id}` - xóa danh mục (admin)

### 2.3 Customer
- `POST /customers/` - đăng ký khách hàng
- `POST /customers/login` - đăng nhập và lấy token
- `POST /customers/token` - token OAuth2
- `GET /customers/` - lấy tất cả khách hàng (admin)
- `GET /customers/{customer_id}` - lấy thông tin khách hàng (phải là chính chủ)
- `PUT /customers/{customer_id}` - cập nhật khách hàng (chính chủ)
- `DELETE /customers/{customer_id}` - xóa khách hàng (chính chủ)

### 2.4 Order
- `POST /orders/` - tạo đơn hàng
- `GET /orders/` - lấy đơn hàng của khách hiện tại
- `GET /orders/{order_id}` - lấy chi tiết đơn hàng (chính chủ)
- `DELETE /orders/{order_id}` - xóa đơn hàng (chính chủ)

### 2.5 Address
- `POST /addresses/` - thêm địa chỉ mới
- `GET /addresses/customer/{customer_id}` - lấy địa chỉ của khách hàng
- `DELETE /addresses/{address_id}` - xóa địa chỉ

### 2.6 Wishlist
- `POST /wishlists/` - thêm vào wishlist
- `GET /wishlists/customer/{customer_id}` - lấy wishlist của khách hàng
- `DELETE /wishlists/{wishlist_id}` - xóa item wishlist

### 2.7 Review
- `POST /reviews/` - thêm đánh giá sản phẩm
- `GET /reviews/product/{product_id}` - lấy đánh giá theo sản phẩm
- `GET /reviews/customer/{customer_id}` - lấy đánh giá của khách hàng

### 2.8 Payment Method
- `GET /payment-methods/` - lấy danh sách phương thức thanh toán
- `GET /payment-methods/{payment_method_id}` - lấy chi tiết phương thức
- `POST /payment-methods/` - tạo phương thức mới (admin)
- `PUT /payment-methods/{payment_method_id}` - cập nhật phương thức (admin)
- `DELETE /payment-methods/{payment_method_id}` - xóa phương thức (admin)

### 2.9 Admin
- `POST /admin/login` - đăng nhập admin
- `GET /admin/products` - lấy sản phẩm cho admin
- `GET /admin/orders` - lấy đơn hàng cho admin
- `PATCH /admin/orders/{order_id}/status` - cập nhật trạng thái đơn hàng

## 3. Model dữ liệu quan trọng

### Product
- `product_id`
- `product_name`
- `description`
- `image_url`
- `unit_price`
- `category_id`
- `discount_percent`
- `stock_quantity`
- `rating_avg`
- `total_reviews`

### Category
- `category_id`
- `category_name`
- `description`

### Customer
- `customer_id`
- `customer_name`
- `customer_email`
- `phone_number`
- `address`
- `is_active`

### Order
- `order_id`
- `customer_id`
- `payment_method_id`
- `items` (list gồm `product_id`, `quantity`)
- `order_date`
- `status`
- `shipping_address`
- `shipping_fee`
- `discount_amount`

### Address
- `address_id`
- `customer_id`
- `street`, `city`, `district`, `zipcode`
- `is_default`

### Wishlist
- `wishlist_id`
- `customer_id`
- `product_id`

### Review
- `review_id`
- `product_id`
- `customer_id`
- `rating`
- `comment`

### Payment Method
- `payment_method_id`
- `mode_name`
- `pay_date`

## 4. Authentication

### Khách hàng
- Đăng nhập: `POST /customers/login` hoặc `POST /customers/token`
- Token JWT trả về `access_token`
- Mỗi request cần dùng header: `Authorization: Bearer <token>`
- Khi lấy hoặc sửa dữ liệu cá nhân cần dùng token và người dùng phải là chính chủ

### Lưu ý CORS
Backend đã cấu hình CORS cho `http://localhost:5500` và `http://localhost:8000`, nên frontend dev có thể chạy trên Live Server hoặc port 8000.

## 5. Roadmap frontend theo cấp

### Cấp 1: Hiển thị dữ liệu và điều hướng cơ bản
- Tạo phần `home` để hiển thị trang chủ
- Tạo phần `products` để hiển thị danh sách sản phẩm
- Tạo phần `product-detail` để hiển thị chi tiết sản phẩm
- Tạo phần `customer` để hiển thị form login/register
- Kết nối các phần bằng link giữa các trang
- Gọi API:
  - `GET /categories/`
  - `GET /products/`
  - `GET /products/{product_id}`

### Cấp 2: Thêm chức năng người dùng và giỏ hàng
- Tạo form đăng ký `POST /customers/`
- Tạo form đăng nhập `POST /customers/login`
- Lưu token vào LocalStorage
- Thêm giỏ hàng local (add/remove/update)
- Tải phương thức thanh toán `GET /payment-methods/`
- Tạo checkout gọi `POST /orders/`
- Hiển thị đơn hàng của khách:
  - `GET /orders/`

### Cấp 3: Profile, wishlist, địa chỉ, đánh giá
- Trang profile khách hàng
  - `GET /customers/{customer_id}`
  - `PUT /customers/{customer_id}`
- Quản lý địa chỉ
  - `POST /addresses/`
  - `GET /addresses/customer/{customer_id}`
  - `DELETE /addresses/{address_id}`
- Wishlist
  - `POST /wishlists/`
  - `GET /wishlists/customer/{customer_id}`
  - `DELETE /wishlists/{wishlist_id}`
- Review sản phẩm
  - `POST /reviews/`
  - `GET /reviews/product/{product_id}`

### Cấp 4: Hoàn thiện UX và logic thực tế
- Thêm filter / search sản phẩm theo danh mục
- Hiển thị rating và đánh giá trong trang chi tiết
- Hiển thị trạng thái đơn hàng
- Quản lý địa chỉ mặc định
- Hiển thị tổng tiền, phí ship, khuyến mãi
- Xử lý lỗi API và thông báo người dùng

## 5.1 Chia theo loại tài nguyên: html / css / js

Mình sẽ hướng dẫn bạn làm theo cách này: mỗi loại file nằm trong một thư mục riêng.

### 5.1.1 Tạo cấu trúc thư mục
Tạo 3 thư mục chính dưới `frontend/`:
- `frontend/html/`
- `frontend/css/`
- `frontend/js/`

### 5.1.2 Tạo các file cần thiết
Tạo các file HTML:
- `frontend/html/index.html`
- `frontend/html/products.html`
- `frontend/html/product-detail.html`
- `frontend/html/cart.html`
- `frontend/html/checkout.html`
- `frontend/html/customer-login.html`

Tạo các file CSS tương ứng:
- `frontend/css/home.css`
- `frontend/css/products.css`
- `frontend/css/product-detail.css`
- `frontend/css/cart.css`
- `frontend/css/checkout.css`
- `frontend/css/customer.css`

Tạo các file JS tương ứng:
- `frontend/js/home.js`
- `frontend/js/products.js`
- `frontend/js/product-detail.js`
- `frontend/js/cart.js`
- `frontend/js/checkout.js`
- `frontend/js/customer.js`

### 5.1.3 Kết nối HTML với CSS và JS
Trong mỗi file HTML, dùng đường dẫn tương đối:
- CSS: `../css/<tên-file>.css`
- JS: `../js/<tên-file>.js`

Ví dụ `frontend/html/products.html`:
```html
<link rel="stylesheet" href="../css/products.css">
<script defer src="../js/products.js"></script>
```

### 5.1.4 Tạo file HTML cơ bản cho mỗi trang
Mỗi file HTML chỉ cần cấu trúc như sau:
```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tên trang</title>
  <link rel="stylesheet" href="../css/<tên-file>.css">
</head>
<body>
  <nav>
    <a href="index.html">Home</a>
    <a href="products.html">Products</a>
    <a href="cart.html">Cart</a>
    <a href="customer-login.html">Customer</a>
  </nav>

  <main id="app"></main>

  <script defer src="../js/<tên-file>.js"></script>
</body>
</html>
```

### 5.1.5 Tạo helper API chung
Tạo một file trong `frontend/js/` (ví dụ `frontend/js/api.js`) nếu bạn muốn dùng chung hàm gọi API:
```js
const API_BASE = 'http://localhost:8000';

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  return res.json();
}

async function apiPost(path, body, token) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  });
  return res.json();
}
```
Nếu dùng `api.js`, import hoặc nhúng nó trước các file JS khác.

### 5.1.6 Hướng dẫn từng bước theo cấp

#### Cấp 1: tạo giao diện và gọi API cơ bản
1. Tạo các file HTML:
   - `frontend/html/index.html`
   - `frontend/html/products.html`
   - `frontend/html/product-detail.html`
   - `frontend/html/customer-login.html`
2. Tạo các file CSS tương ứng. Mỗi file chỉ cần CSS cơ bản cho layout, font, và card sản phẩm.
3. Tạo các file JS tương ứng. Mỗi file nên có hàm `initPage()` gọi khi tải trang.
4. Trong `frontend/js/products.js`:
   - gọi `GET /categories/`
   - gọi `GET /products/`
   - render danh sách sản phẩm ra HTML
   - mỗi sản phẩm có link tới `product-detail.html?id=<product_id>`

   Ví dụ:
   ```js
   async function initPage() {
     const products = await apiGet('/products/');
     const app = document.getElementById('app');
     app.innerHTML = products.map(product => `
       <div class="product-card">
         <img src="${product.image_url || 'https://via.placeholder.com/200'}" alt="${product.product_name}">
         <h2>${product.product_name}</h2>
         <p>${product.unit_price}</p>
         <a href="product-detail.html?id=${product.product_id}">Xem chi tiết</a>
       </div>
     `).join('');
   }
   initPage();
   ```
5. Trong `frontend/js/product-detail.js`:
   - đọc `id` từ query string
   - gọi `GET /products/{product_id}`
   - hiển thị tên, ảnh, giá, danh mục, mô tả

   Ví dụ:
   ```js
   const params = new URLSearchParams(window.location.search);
   const productId = params.get('id');
   async function initPage() {
     const product = await apiGet(`/products/${productId}`);
     document.getElementById('app').innerHTML = `...`; 
   }
   initPage();
   ```
6. Trong `frontend/js/customer.js`:
   - tạo form đăng ký và form đăng nhập
   - submit gọi `POST /customers/` và `POST /customers/login`
   - lưu token vào `localStorage.setItem('token', access_token)`
   - dùng token để xác thực các trang sau

#### Cấp 2: thêm giỏ hàng và checkout
1. Tạo `frontend/html/cart.html` và `frontend/js/cart.js`
   - dùng `localStorage` để lưu giỏ hàng
   - các hàm cơ bản: `getCart()`, `saveCart(cart)`, `addToCart(item)`, `removeFromCart(id)`, `updateQuantity(id, qty)`
2. Trong `products.js` và `product-detail.js` thêm nút "Thêm vào giỏ".
   - khi click gọi `addToCart()` và lưu vào localStorage.
3. Tạo `frontend/html/checkout.html` và `frontend/js/checkout.js`
   - gọi `GET /payment-methods/`
   - hiển thị form chọn phương thức thanh toán
   - khi submit tạo payload order:
     ```json
     {
       "customer_id": "<customer_id>",
       "payment_method_id": "<payment_method_id>",
       "items": [
         {"product_id": "...", "quantity": 2}
       ]
     }
     ```
   - gọi `POST /orders/` với token
4. Tạo thêm trang `frontend/html/orders.html` và `frontend/js/orders.js`
   - gọi `GET /orders/` với token
   - hiển thị danh sách đơn hàng của khách

#### Cấp 3: profile, wishlist, địa chỉ, review
1. Tạo `frontend/html/profile.html` và `frontend/js/profile.js`
   - gọi `GET /customers/{customer_id}`
   - hiển thị thông tin khách hàng
   - cho phép cập nhật qua `PUT /customers/{customer_id}`
2. Tạo `frontend/html/addresses.html` và `frontend/js/addresses.js`
   - gọi `GET /addresses/customer/{customer_id}`
   - thêm địa chỉ bằng `POST /addresses/`
   - xóa bằng `DELETE /addresses/{address_id}`
3. Tạo `frontend/html/wishlist.html` và `frontend/js/wishlist.js`
   - gọi `GET /wishlists/customer/{customer_id}`
   - thêm item bằng `POST /wishlists/`
   - xóa item bằng `DELETE /wishlists/{wishlist_id}`
4. Tạo `frontend/html/reviews.html` hoặc mở rộng `product-detail.html`
   - gọi `GET /reviews/product/{product_id}`
   - gửi đánh giá bằng `POST /reviews/`

#### Cấp 4: hoàn thiện UX và logic thực tế
1. Trong `frontend/js/products.js` thêm:
   - lọc theo category
   - tìm kiếm theo tên
   - sắp xếp theo giá hoặc rating
2. Trong `frontend/js/product-detail.js` hiển thị:
   - rating trung bình
   - review list
   - nút thêm wishlist
3. Trong `frontend/js/orders.js` hiển thị:
   - trạng thái đơn hàng
   - ngày đặt hàng
4. Trong `frontend/js/checkout.js` tính toán:
   - tổng tiền sản phẩm
   - phí ship
   - khuyến mãi
5. Trong mọi file JS xử lý lỗi API:
   - nếu fetch lỗi hoặc trả 401 thì hiện thông báo
   - nếu token hết hạn, chuyển về trang login

### 5.1.7 Giữ các file CSS và JS rõ ràng
- `home.css` chỉ chứa style cho trang chủ
- `products.css` chỉ chứa style cho danh sách sản phẩm
- `product-detail.css` chỉ chứa style cho chi tiết sản phẩm
- `cart.css` chỉ chứa style cho giỏ hàng
- `checkout.css` chỉ chứa style cho trang thanh toán
- `customer.css` chứa style cho login/register và profile

- `home.js` chỉ xử lý logic trang chủ
- `products.js` xử lý gọi API sản phẩm và render danh sách
- `product-detail.js` xử lý gọi API chi tiết sản phẩm và review
- `cart.js` xử lý localStorage giỏ hàng
- `checkout.js` xử lý tạo đơn và thanh toán
- `customer.js` xử lý đăng ký / đăng nhập / lưu token

## 6. Bắt đầu code từ đâu

1. Mở `frontend_demo/` để tham khảo giao diện sẵn có.
2. Dùng `frontend_demo/index.html`, `products.html`, `product-detail.html`, `cart.html`, `checkout.html`, `customer-login.html` làm khuôn.
3. Thay từng phần mock data bằng fetch API vào backend.
4. Chạy backend với `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
5. Mở frontend trên Live Server hoặc `python -m http.server`.

## 7. Kiểm tra nhanh

- Trang backend chạy: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- CORS đã bật cho frontend dev

## 8. Gợi ý tên file frontend cần thiết

- `index.html` - trang chủ
- `products.html` - danh sách sản phẩm
- `product-detail.html` - chi tiết sản phẩm
- `cart.html` - giỏ hàng
- `checkout.html` - thanh toán
- `customer-login.html` - đăng nhập/đăng ký
- `css/style.css` - kiểu chung
- `js/app.js` - logic chung với fetch API và quản lý state

---

> File này là tài liệu hướng dẫn cho bạn bắt đầu code frontend dựa vào backend hiện tại. Nếu muốn, mình có thể tiếp tục tạo cho bạn một phiên bản `app.js` mẫu để gọi API chính ngay.