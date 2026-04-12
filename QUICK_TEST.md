# 🚀 QUICK START - RUN & TEST

## ⚡ BƯỚC 1: KHỞI ĐỘNG BACKEND

```bash
cd c:\Users\Admin\Documents\PROJECT_IT\Sale_Web_Project\backend
python -m uvicorn app.main:app --reload
```

✅ Xác nhận: `Uvicorn running on http://127.0.0.1:8000`

---

## ⚡ BƯỚC 2: KHỞI ĐỘNG FRONTEND

**Mở terminal mới:**

```bash
cd c:\Users\Admin\Documents\PROJECT_IT\Sale_Web_Project\frontend_demo
python -m http.server 5500
```

✅ Xác nhận: Server running on port 5500

---

## ⚡ BƯỚC 3: MỞ TRÌNH DUYỆT

### **Test API Backend:**
```
http://127.0.0.1:8000/docs
```
(Swagger UI - test endpoints trực tiếp)

### **Test Frontend:**
```
http://127.0.0.1:5500
```

---

## 🧪 FLOW TEST

### **1. Đăng Ký Tài Khoản**
- Truy cập: `http://127.0.0.1:5500/customer-login.html`
- Click "Đăng ký ngay"
- Điền thông tin:
  - Họ tên: `Nguyen Van Test`
  - Email: `test@example.com`
  - SĐT: `0987654321`
  - Mật khẩu: `123456`
- Click "Tạo tài khoản"
- ✅ Thấy dashboard → Success!

### **2. Đăng Nhập**
- Click "Đăng nhập"
- Email: `test@example.com`
- Password: `123456`
- Click "Đăng nhập"
- ✅ Thấy dashboard → Success!

### **3. Xem Sản Phẩm**
- Truy cập: `http://127.0.0.1:5500`
- ✅ Thấy sản phẩm từ API (không phải dữ liệu mock)

### **4. Thêm Giỏ Hàng**
- Click sản phẩm bất kỳ
- Click "Thêm vào giỏ"
- ✅ Số lượng trong 🛒 tăng lên

### **5. THANH TOÁN (PHẦN SỬA LỖI)**
- Click 🛒 → "Tiến hành thanh toán"
- **BƯỚC 1: Điền Thông Tin**
  - ✅ Phải điền TẤT CẢ 7 trường:
    - Họ tên
    - Email
    - SĐT
    - Địa chỉ
    - **Thành phố** (Chọn từ dropdown)
    - **Quận/Huyện**
    - **Mã bưu chính**
  - Click "Tiếp tục → Chọn thanh toán"
  - ✅ Chuyển sang bước 2

- **BƯỚC 2: Chọn Thanh Toán**
  - Chọn 1 option (VD: "Thanh toán khi nhận hàng")
  - Click "Tiếp tục → Xác nhận"
  - ✅ Chuyển sang bước 3

- **BƯỚC 3: Xác Nhận**
  - Tick "☑️ Tôi đồng ý..."
  - Click "HOÀN TẬT ĐƠN HÀNG"
  - ✅ Thấy thông báo success + mã đơn hàng

### **6. Kiểm Tra Database**

```bash
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d retail_db
```

**Chạy:**
```sql
SELECT customer_id, customer_name, customer_email FROM customers 
WHERE customer_email = 'test@example.com';

SELECT order_id, customer_id, order_date FROM orders;

SELECT * FROM order_items;

SELECT * FROM payment_methods;
```

✅ Thấy dữ liệu mới → Success!

---

## 🔍 DEBUGGING

**Mở DevTools (F12):**
- Console: Xem logs
- Network: Xem API calls
- Application: Xem localStorage

---

## 📋 CHECKLIST NHANH

- [ ] Backend chạy ✓
- [ ] Frontend chạy ✓
- [ ] Đăng ký account ✓
- [ ] Đăng nhập ✓
- [ ] Xem sản phẩm ✓
- [ ] Thêm giỏ ✓
- [ ] Checkout bước 1 ✓
- [ ] Checkout bước 2 ✓
- [ ] Checkout bước 3 ✓
- [ ] Database có dữ liệu ✓

**Tất cả ✓ = Project hoạt động 100%! 🎉**

---

## 🆘 TROUBLESHOOTING NHANH

| Lỗi | Cách Sửa |
|-----|----------|
| Port 8000 busy | `netstat -ano \| findstr :8000` → Kill PID |
| Cannot connect DB | Check PostgreSQL running |
| CORS error | Backend CORS config OK |
| Thanh toán không chuyển bước | Điền TẤT CẢ 7 trường (không bỏ qua thành phố, quận, mã bưu chính) |
| getCart() not found | Đảm bảo app.js load trước checkout.html |

---

Hãy **test ngay bây giờ!** 🚀
