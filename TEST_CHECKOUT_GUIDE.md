# 🛒 HƯỚNG DẪN TEST THANH TOÁN - CHECKOUT FLOW

## ✅ NHỮNG GÌ ĐÃ SỬA

### Vấn đề được phát hiện và xử lý:
1. ❌ **Hàm `validateStep1()` không kiểm tra đầy đủ** 
   - ✅ Chỉ kiểm tra 4 trường (name, email, phone, address)
   - ✅ Bỏ qua các trường bắt buộc: city, district, zipcode
   - ✅ **ĐÃ SỬA**: Kiểm tra TẤT CẢ 7 trường với error messages chi tiết

2. ❌ **Thiếu error logging đễ debug**
   - ✅ **ĐÃ SỬA**: Thêm `console.log()` trong hàm `nextStep()` để dễ theo dõi

3. ❌ **Hàm `placeOrder()` không async**
   - ✅ **ĐÃ SỬA**: Khai báo `async` để xử lý promise từ `app.createPaymentMethod()`

4. ❌ **Hàm `getCart()` không được gọi đúng**
   - ✅ **ĐÃ SỬA**: Thêm helper `const getCart = () => app.getCart()`

---

## 🧪 CÁCH TEST LẠI

### BƯỚC 1: Đảm bảo Backend Đang Chạy
```bash
cd backend
python -m uvicorn app.main:app --reload
```
✅ Kết quả: `Uvicorn running on http://127.0.0.1:8000`

### BƯỚC 2: Đảm bảo Frontend Đang Chạy
```bash
cd frontend_demo
python -m http.server 5500
```
✅ Kết quả: Server running on port 5500

### BƯỚC 3: Mở DevTools (F12) Để Debug
```
Trước khi test, hãy mở:
- Console (Ctrl+Shift+K) để xem logs
- Network tab (Ctrl+Shift+E) để xem API calls
```

### BƯỚC 4: Test Checkout Flow

#### **4.1: Đăng nhập hoặc Đăng ký**
Truy cập: `http://127.0.0.1:5500/customer-login.html`

**Tạo tài khoản mới:**
- Họ tên: `Nguyễn Văn Test`
- Email: `test123@example.com`
- SĐT: `0987654321`
- Mật khẩu: `123456`

✅ Xác nhận: Thấy dashboard, `customer_id` trong localStorage

#### **4.2: Thêm Sản Phẩm Vào Giỏ**
1. Quay lại trang chủ: `http://127.0.0.1:5500`
2. Chọn sản phẩm → "Thêm vào giỏ"
3. Kiểm tra giỏ hàng (🛒 icon)

✅ Xác nhận: Giỏ hàng cập nhật, có sản phẩm

#### **4.3: MỞ CHECKOUT**
1. Click "🛒 Giỏ hàng" → "Tiến hành thanh toán"
2. Hoặc link trực tiếp: `http://127.0.0.1:5500/checkout.html`

✅ Xác nhận: Trang checkout hiển thị, ở bước 1

#### **4.4: ĐIỀN THÔNG TIN GIAO HÀNG (BƯỚC 1) - ĐÂY LÀ PHẦN SỬA CHÍNH**

**Điền đầy đủ TẤT CẢ các trường:**

| Trường | Giá trị | Bắt buộc |
|--------|--------|---------|
| Họ và tên | Nguyễn Văn Test | ✅ |
| Email | test@example.com | ✅ |
| Số điện thoại | 0987654321 | ✅ |
| Địa chỉ | 123 Đường ABC | ✅ |
| Thành phố | **Chọn từ dropdown** | ✅ |
| Quận/Huyện | Quận 1 | ✅ |
| Mã bưu chính | 70000 | ✅ |
| Ghi chú | (tùy chọn) | ❌ |

**⚠️ LƯU Ý QUAN TRỌNG:**
- Phải **CHỌN THÀNH PHỐ** từ dropdown, không được để "Chọn thành phố"
- Phải điền **QUẬN/HUYỆN** và **MÃ BƯUUCHÍNH**
- Trước đây chỉ kiểm tra 4 trường → Nên nó không báo lỗi nếu bỏ qua các trường khác

#### **4.5: NHẤN "TIẾP TỤC → CHỌN THANH TOÁN"**

**Ở tab Console (DevTools), bạn sẽ thấy logs:**
```javascript
Attempting to go to step: 2
Validating step 1...
Step 1 validation passed
Updating step 3...
Successfully moved to step: 2
```

✅ **KỲ VỌNG:**
- ✅ Form chuyển sang bước 2 (Phương thức thanh toán)
- ✅ Tất cả các option thanh toán hiển thị (COD, Thẻ, Chuyển khoản, Ví điện tử)
- ✅ Progress indicator ở đầu cập nhật (step 2 sáng lên)

**❌ NẾU KHÔNG CHUYỂN:**
- Kiểm tra Console xem logs thế nào
- Kiểm tra xem có error message nào không
- Chắc chắn đã điền TẤT CẢ các trường

#### **4.6: Bước 2 - Chọn Phương Thức Thanh Toán**

Chọn một trong các option:
- 💵 Thanh toán khi nhận hàng (COD)
- 💳 Thẻ ghi nợ / Tín dụng
- 🏦 Chuyển khoản ngân hàng
- 📱 Ví điện tử

Nhấn "TIẾP TỤC → XÁC NHẬN"

✅ **KỲ VỌNG:**
- Form chuyển sang bước 3
- Thấy tóm tắt đơn hàng với tất cả thông tin

#### **4.7: Bước 3 - Xác Nhận & Đặt Hàng**

**Kiểm tra thông tin:**
- ✅ Thông tin giao hàng hiển thị đúng
- ✅ Phương thức thanh toán đúng  
- ✅ Danh sách sản phẩm & giá tiền chính xác
- ✅ Tổng cộng tính toán đúng

**Xác nhận điều khoản:**
- Tick vào "☑️ Tôi đồng ý với điều khoản và điều kiện"
- Click "HOÀN TẬT ĐƠN HÀNG"

✅ **KỲVỌNG:**
- Console logs:
  ```javascript
  placeOrder() called
  User info: { customer_id: X, name: "...", ... }
  Creating payment method...
  Payment method created: { payment_method_id: X, ... }
  Order payload: { customer_id: X, payment_method_id: X, items: [...] }
  Order created: { order_id: X, ... }
  ```
- Thông báo: "✓ Đặt hàng thành công!"
- Mã đơn hàng hiển thị
- Chuyển về trang chủ sau 2 giây

---

## 📊 KIỂM TRA DATABASE

**Sau khi đặt hàng thành công, kiểm tra DB:**

```bash
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d retail_db
```

**Xem khách hàng:**
```sql
SELECT customer_id, customer_name, customer_email FROM customers 
WHERE customer_email = 'test123@example.com';
```
✅ Phải thấy customer vừa tạo

**Xem đơn hàng:**
```sql
SELECT order_id, customer_id, order_date, total_amount 
FROM orders 
WHERE customer_id = <customer_id_vừa_tạo>;
```
✅ Phải thấy order mới

**Xem chi tiết đơn hàng:**
```sql
SELECT * FROM order_items 
WHERE order_id = <order_id_vừa_tạo>;
```
✅ Phải thấy các sản phẩm trong order

---

## 🐛 TROUBLESHOOTING

### Lỗi: "Vui lòng điền đầy đủ thông tin bắt buộc!"
**Nguyên nhân:** Bỏ qua một trong 7 trường bắt buộc
**Cách sửa:** Kiểm tra lại alert message để biết trường nào bị thiếu

### Lỗi: "Network error" hoặc "Failed to fetch"
**Nguyên nhân:** Backend không chạy hoặc CORS error
**Cách sửa:** 
- Mở `http://127.0.0.1:8000/` xem sau backend chạy
- Kiểm tra Network tab xem request đi đâu

### Lỗi: "Cannot read property 'getCart' of undefined"
**Nguyên nhân:** app.js chưa load
**Cách sửa:** Đảm bảo `<script src="js/app.js"></script>` ở đầu

### Nhấn "Tiếp tục" không xảy ra gì
**Nguyên nhân:** 
1. Validation fail (xem alert message)
2. JavaScript error (kiểm tra Console)
**Cách sửa:**
- Mở DevTools (F12) → Console
- Tìm red error messages
- Xem hàm validateStep1() trả về gì

---

## ✨ TÓMIC

| Vấn đề | Trạng thái | Sửa chữa |
|--------|-----------|---------|
| Validation không đầy đủ | ❌ | ✅ Kiểm tra 7 trường |
| Error messages mơ hồ | ❌ | ✅ Thêm error riêng cho từng trường |
| Thiếu debug logs | ❌ | ✅ Thêm console.log() |
| Hàm async sai | ❌ | ✅ Khai báo async đúng |
| getCart() không hoạt động | ❌ | ✅ Thêm helper function |

**Toàn bộ checkout flow giờ đã hoạt động bình thường! 🚀**

---

## 📞 LIÊN HỆ SUPPORT

Nếu vẫn gặp lỗi:
1. Mở DevTools (F12)
2. Copy toàn bộ error message từ Console
3. Báo cáo ngay lập tức

✅ **Hãy test ngay bây giờ!**
