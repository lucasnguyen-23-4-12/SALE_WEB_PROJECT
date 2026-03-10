# Tech Store Frontend Demo

Một ứng dụng web bán lẻ điện tử (e-commerce) được xây dựng bằng HTML5, CSS3 và JavaScript vanilla. Đây là phần giao diện người dùng (UI/UX) hoàn chỉnh cho một cửa hàng bán các sản phẩm công nghệ.

## 📁 Cấu trúc thư mục

```
frontend_demo/
├── index.html                 # Trang chủ
├── products.html              # Trang danh sách sản phẩm
├── product-detail.html        # Chi tiết sản phẩm
├── cart.html                  # Giỏ hàng
├── checkout.html              # Trang thanh toán
├── customer-login.html        # Tài khoản/Đăng nhập
├── css/
│   └── style.css              # Stylesheet chính
├── js/
│   └── app.js                 # JavaScript chính
└── images/                    # Thư mục ảnh (sẽ được thêm sau)
```

## 🎨 Các trang chính

### 1. **Trang chủ (index.html)**
- Banner quảng cáo chính
- Các danh mục sản phẩm (Categories)
- Sản phẩm nổi bật (Featured Products)
- Khuyến mãi đặc biệt

### 2. **Danh sách sản phẩm (products.html)**
- Lưới sản phẩm responsive
- Bộ lọc theo danh mục, giá, đánh giá
- Sắp xếp sản phẩm (giá, đánh giá, mới nhất)
- Thanh tìm kiếm (sẵn sàng để tích hợp)

### 3. **Chi tiết sản phẩm (product-detail.html)**
- Xem ảnh sản phẩm (zoom, thumbnails)
- Thông tin chi tiết
- Bảng giá so sánh
- Chọn số lượng
- Đánh giá và bình luận từ khách hàng
- Sản phẩm liên quan (Recommendations)

### 4. **Giỏ hàng (cart.html)**
- Danh sách sản phẩm trong giỏ
- Tính tổng tiền, vận chuyển, chiết khấu
- Nhập mã khuyến mãi
- Gợi ý sản phẩm thêm
- Liên kết tới thanh toán

### 5. **Thanh toán (checkout.html)**
- **Bước 1:** Thông tin giao hàng (FillIn Form)
- **Bước 2:** Chọn phương thức thanh toán (COD, Thẻ, Chuyển khoản, E-wallet)
- **Bước 3:** Xác nhận đơn hàng
- Tính toán tổng tiền tự động

### 6. **Tài khoản (customer-login.html)**
- **Đăng nhập:** Form đăng nhập
- **Đăng ký:** Tạo tài khoản mới
- **Dashboard:** Xem đơn hàng, thông tin cá nhân, địa chỉ, danh sách yêu thích

## 🚀 Chức năng chính

### Frontend Features
1. ✅ Quản lý giỏ hàng (Add, Update, Remove)
2. ✅ Tìm kiếm và lọc sản phẩm
3. ✅ Sắp xếp sản phẩm theo nhiều tiêu chí
4. ✅ Xem chi tiết sản phẩm
5. ✅ Đánh giá sản phẩm
6. ✅ Hệ thống tài khoản người dùng
7. ✅ Quy trình thanh toán đầy đủ
8. ✅ Danh sách yêu thích
9. ✅ Lịch sử đơn hàng

### Storage & Data
- Sử dụng **LocalStorage** để lưu giỏ hàng, tài khoản, đơn hàng
- Mock data cho 12+ sản phẩm
- Dữ liệu tự động cập nhật mà không cần reload

## 🔧 Cách sử dụng

### 1. Mở trực tiếp
```bash
# Chỉ cần mở file index.html trong trình duyệt
# hoặc dùng Live Server extension
```

### 2. Với Live Server (VS Code)
```bash
# Cài đặt extension "Live Server"
# Click chuột phải trên index.html → Open with Live Server
# Website sẽ tự động mở tại http://127.0.0.1:5500
```

### 3. Với Python
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Truy cập http://localhost:8000/frontend_demo/
```

### 4. Với Node.js
```bash
# Cài đặt http-server
npm install -g http-server

# Chạy
http-server frontend_demo/

# Truy cập http://127.0.0.1:8080
```

## 📱 Responsive Design

Trang web hoàn toàn responsive trên:
- 💻 Desktop (1200px+)
- 📱 Tablet (768px - 1199px)
- 📲 Mobile (< 768px)

## 🎯 Sản phẩm Mock

Danh sách 12 sản phẩm giả không bao gồm:

| ID | Tên sản phẩm | Danh mục | Giá | Discount |
|----|---|---|---|---|
| 1 | iPhone 15 Pro Max | Smartphones | 28M | 20% |
| 2 | Samsung Galaxy S24 Ultra | Smartphones | 26M | 21% |
| 3 | MacBook Pro 16" | Computers | 45M | 20% |
| 4 | Dell XPS 15 | Computers | 35M | 17% |
| 5 | AirPods Pro 2 | Accessories | 6.5M | 19% |
| 6 | Sony WH-1000XM5 | Accessories | 7.2M | 20% |
| 7 | Apple Watch Series 9 | Wearables | 12M | 20% |
| 8 | Google Pixel Watch 2 | Wearables | 9.5M | 19% |
| ... | ... | ... | ... | ... |

## 🔌 Chuẩn bị tích hợp API Backend

### Quy trình tích hợp (sẽ được thực hiện sau):

1. **Thay thế Mock Data** bằng API calls
```javascript
// Hiện tại
const mockProducts = [...];

// Sau khi tích hợp backend
fetchProductsFromAPI()
  .then(data => renderProducts(data))
```

2. **Endpoints cần thiết từ Backend**:
   - `GET /categories/` - Lấy danh mục
   - `GET /products/` - Lấy sản phẩm (& filter, sort)
   - `GET /products/{id}/` - Chi tiết sản phẩm
   - `POST /orders/` - Tạo đơn hàng
   - `GET /customers/` - Thông tin khách hàng
   - `POST /auth/login/` - Đăng nhập
   - `POST /auth/register/` - Đăng ký

3. **Authentication**:
   - Sử dụng JWT tokens
   - LocalStorage lưu token
   - Header `Authorization: Bearer <token>`

## 🎨 Tùy chỉnh giao diện

### Màu sắc chính (trong `css/style.css`):
```css
:root {
    --primary-color: #007bff;      /* Xanh dương */
    --secondary-color: #6c757d;    /* Xám */
    --success-color: #28a745;      /* Xanh lá */
    --danger-color: #dc3545;       /* Đỏ */
}
```

### Font chữ:
```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

## ⚠️ Lưu ý

1. **Dữ liệu tạm thời**: Tất cả dữ liệu được lưu trong LocalStorage, sẽ mất khi xóa cache
2. **Không có kết nối backend**: Hiện tại chỉ là giao diện UI, chưa kết nối API thực tế
3. **Ảnh sản phẩm**: Sử dụng placeholder từ `via.placeholder.com`, thay thế bằng ảnh thực tế sau
4. **Tài khoản giả**: Demo sử dụng tài khoản giả, cần backend xác thực thực tế

## 📝 TODOs (Phát triển tiếp)

- [ ] Kết nối API backend (FastAPI)
- [ ] Tải ảnh sản phẩm từ server
- [ ] Tích hợp thanh toán thực (Stripe, VNPAY, v.v.)
- [ ] Thêm tìm kiếm sản phẩm
- [ ] Gửi email xác nhận đơn hàng
- [ ] Bản đồ Google để chọn địa chỉ
- [ ] Rating sao và bình luận từ backend
- [ ] Hệ thống coupon/khuyến mãi
- [ ] Chat hỗ trợ khách hàng (Live Chat)
- [ ] Dark mode

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra console (F12 → Console tab)
2. Xóa cache/LocalStorage nếu dữ liệu bị lỗi
3. Đảm bảo truy cập qua HTTP server, không phải file://

---

**Phiên bản:** 1.0.0 Demo  
**Ngày tạo:** March 2026  
**Trạng thái:** Sẵn sàng tích hợp backend
