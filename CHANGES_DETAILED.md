# 🔧 TÓMIC CÁC THAY ĐỔI CHI TIẾT

## 📌 BACKEND CHANGES

### 1️⃣ **File: `backend/app/schemas/customer.py`**

**Thêm:**
```python
# Login
class CustomerLogin(BaseModel):
    email_or_phone: str
    password: str
```

**Lý do:** Cần schema riêng cho login endpoint để nhận email_or_phone và password

---

### 2️⃣ **File: `backend/app/services/customer_service.py`**

**Thêm hàm:**
```python
def authenticate_customer(db: Session, email_or_phone: str, password: str):
    """Xác thực customer bằng email/phone và password"""
    customer = db.query(Customer).filter(
        (Customer.customer_email == email_or_phone) |
        (Customer.phone_number == email_or_phone)
    ).first()

    if not customer:
        raise NotFoundException("Customer")

    if customer.password_hash != hash_password(password):
        raise ValidationException("Invalid password")

    return customer
```

**Lý do:** Backend cần hàm xác thực để kiểm tra credentials

---

### 3️⃣ **File: `backend/app/routers/customer_router.py`**

**Thêm import:**
```python
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerLogin  # ← Thêm
)
```

**Thêm endpoint:**
```python
@router.post(
    "/login",
    response_model=CustomerResponse
)
def login_customer(
    payload: CustomerLogin,
    db: Session = Depends(get_db)
):
    return customer_service.authenticate_customer(
        db, payload.email_or_phone, payload.password
    )
```

**Lý do:** Frontend cần endpoint để đăng nhập

---

## 📌 FRONTEND CHANGES

### 4️⃣ **File: `frontend_demo/js/app.js`**

**Thêm hàm:**
```javascript
async function loginCustomer(loginData) {
    const res = await fetch(`${API_BASE}/customers/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
    });
    if (!res.ok) throw new Error('Login failed');
    return res.json();
}

async function createPaymentMethod(paymentData) {
    const res = await fetch(`${API_BASE}/payment-methods/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paymentData)
    });
    if (!res.ok) throw new Error('Create payment method failed');
    return res.json();
}
```

**Sửa helpers:**
```javascript
// helpers that ALWAYS call server API (no fallback to mock)
async function loadProductList(skip = 0, limit = 12) {
    return await fetchProducts(skip, limit);
}

async function loadProduct(id) {
    return await fetchProductById(id);
}

async function submitOrder(orderPayload) {
    return await createOrderOnServer(orderPayload);
}
```

**Thêm exports:**
```javascript
window.app = {
    // ... các export khác
    createCustomer,
    loginCustomer,
    createPaymentMethod
};
```

**Lý do:** Frontend cần các hàm này để gọi API backend

---

### 5️⃣ **File: `frontend_demo/customer-login.html`**

**Sửa hàm `handleLogin()`:**
```javascript
function handleLogin() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        alert('Vui lòng điền đầy đủ thông tin!');
        return;
    }

    // Gọi API đăng nhập
    const loginData = {
        email_or_phone: email,
        password: password
    };

    fetch('http://127.0.0.1:8000/customers/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Đăng nhập thất bại');
        }
        return response.json();
    })
    .then(data => {
        // Lưu thông tin customer vào localStorage
        localStorage.setItem('user', JSON.stringify({
            customer_id: data.customer_id,
            name: data.customer_name,
            email: data.customer_email,
            phone: data.phone_number
        }));

        showDashboard();
        alert('✓ Đăng nhập thành công!');
    })
    .catch(error => {
        console.error('Lỗi:', error);
        alert('❌ Sai email/số điện thoại hoặc mật khẩu!');
    });
}
```

**Sửa hàm `handleSignup()`:**
```javascript
function handleSignup() {
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const phone = document.getElementById('signup-phone').value;
    const password = document.getElementById('signup-password').value;
    const confirm = document.getElementById('signup-password-confirm').value;

    if (!name || !email || !phone || !password || !confirm) {
        alert('Vui lòng điền đầy đủ thông tin!');
        return;
    }

    if (password !== confirm) {
        alert('Mật khẩu không trùng khớp!');
        return;
    }

    // Gọi API tạo customer
    const customerData = {
        customer_name: name,
        customer_email: email,
        phone_number: phone,
        address: "",
        password: password
    };

    fetch('http://127.0.0.1:8000/customers/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customerData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Tạo tài khoản thất bại');
        }
        return response.json();
    })
    .then(data => {
        // Lưu thông tin customer vào localStorage
        localStorage.setItem('user', JSON.stringify({
            customer_id: data.customer_id,
            name: data.customer_name,
            email: data.customer_email,
            phone: data.phone_number
        }));

        showDashboard();
        alert('✓ Tạo tài khoản thành công!');
    })
    .catch(error => {
        console.error('Lỗi:', error);
        alert('❌ Lỗi tạo tài khoản. Email có thể đã tồn tại.');
    });
}
```

**Lý do:** Login/Signup phải gọi backend để xác thực & lưu vào DB

---

### 6️⃣ **File: `frontend_demo/checkout.html` - ⭐ PHẦN SỬA LỖI CHÍNH**

**Thêm helper function:**
```javascript
const getCart = () => app.getCart();
```

**Sửa hàm `nextStep()` - Thêm logging:**
```javascript
function nextStep(step) {
    console.log('Attempting to go to step:', step);
    
    if (step === 2) {
        console.log('Validating step 1...');
        if (!validateStep1()) {
            console.log('Step 1 validation failed');
            return;
        }
        console.log('Step 1 validation passed');
    }
    if (step === 3) {
        console.log('Validating step 2...');
        if (!validateStep2()) {
            console.log('Step 2 validation failed');
            return;
        }
        console.log('Updating step 3...');
        updateStep3();
    }

    document.querySelectorAll('.checkout-section').forEach(s => s.classList.remove('active'));
    document.getElementById('step-' + step).classList.add('active');
    document.querySelectorAll('.checkout-steps .step').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.checkout-steps .step')[step - 1].classList.add('active');
    currentStep = step;
    console.log('Successfully moved to step:', step);
    window.scrollTo(0, 0);
}
```

**⭐ SỬA HÀM `validateStep1()` - ĐÂY LÀ LỖI CHÍNH:**
```javascript
function validateStep1() {
    const name = document.getElementById('customer-name').value.trim();
    const email = document.getElementById('customer-email').value.trim();
    const phone = document.getElementById('customer-phone').value.trim();
    const address = document.getElementById('customer-address').value.trim();
    const city = document.getElementById('customer-city').value;
    const district = document.getElementById('customer-district').value.trim();
    const zipcode = document.getElementById('customer-zipcode').value.trim();

    if (!name) {
        alert('❌ Vui lòng nhập Họ và tên!');
        return false;
    }
    if (!email) {
        alert('❌ Vui lòng nhập Email!');
        return false;
    }
    if (!phone) {
        alert('❌ Vui lòng nhập Số điện thoại!');
        return false;
    }
    if (!address) {
        alert('❌ Vui lòng nhập Địa chỉ!');
        return false;
    }
    if (city === 'Chọn thành phố') {
        alert('❌ Vui lòng chọn Thành phố!');
        return false;
    }
    if (!district) {
        alert('❌ Vui lòng nhập Quận/Huyện!');
        return false;
    }
    if (!zipcode) {
        alert('❌ Vui lòng nhập Mã bưu chính!');
        return false;
    }
    return true;
}
```

**⭐ SỬA HÀM `placeOrder()` - Thêm async:**
```javascript
async function placeOrder() {
    console.log('placeOrder() called');
    
    if (!document.getElementById('agree-terms').checked) {
        alert('✋ Vui lòng đồng ý với điều khoản và điều kiện!');
        return;
    }

    // Build order payload matching backend field names
    const cartItems = getCart().map(item => ({
        product_id: item.product_id,
        quantity: item.quantity,
        price_at_purchase: item.unit_price
    }));

    console.log('Cart items:', cartItems);

    const shipping = document.getElementById('confirm-shipping').textContent === 'Miễn phí' ? 0 : 25000;

    // Lấy customer_id từ user đã đăng nhập
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const customerId = user.customer_id || null;

    console.log('User info:', user);
    console.log('Customer ID:', customerId);

    if (!customerId) {
        alert('⚠️ Vui lòng đăng nhập trước khi đặt hàng!');
        window.location.href = 'customer-login.html';
        return;
    }

    // Tạo payment method trước
    const paymentMethodData = {
        mode_name: 'Credit Card',
        pay_date: null
    };

    try {
        console.log('Creating payment method...');
        const paymentMethod = await app.createPaymentMethod(paymentMethodData);
        console.log('Payment method created:', paymentMethod);
        const paymentMethodId = paymentMethod.payment_method_id;

        const orderPayload = {
            customer_id: customerId,
            payment_method_id: paymentMethodId,
            items: cartItems
        };

        console.log('Order payload:', orderPayload);

        // Submit order to backend
        await submitOrderToBackend(orderPayload);
    } catch (error) {
        console.error('Error in placeOrder:', error);
        alert('⚠️ Lỗi: ' + error.message);
    }
}
```

**Lý do:**
1. ❌ Cũ chỉ kiểm tra 4 trường → ✅ Kiểm tra 7 trường
2. ❌ Cũ không async → ✅ Thêm async
3. ❌ Cũ getCart() không tìm → ✅ Thêm helper

---

## 📊 TÓMIC CÁC THAY ĐỔI

| File | Thay đổi | Dòng |
|------|----------|------|
| `backend/app/schemas/customer.py` | Thêm `CustomerLogin` | +5 lines |
| `backend/app/services/customer_service.py` | Thêm `authenticate_customer()` | +18 lines |
| `backend/app/routers/customer_router.py` | Thêm import & endpoint login | +10 lines |
| `frontend_demo/js/app.js` | Thêm 2 hàm API & sửa helpers | +30 lines |
| `frontend_demo/customer-login.html` | Sửa login/signup | ±50 lines |
| `frontend_demo/checkout.html` | ⭐ SỬA LỖI THANH TOÁN | ±60 lines |

**Tổng cộng:** ~170 lines changes, 6 files affected

---

## 🎯 KIỂM ĐỊNH HOẠT ĐỘNG

Sau các sửa chữa:

✅ **Backend:**
- POST /customers/login ✓
- POST /customers/ ✓
- POST /payment-methods/ ✓
- POST /orders/ ✓

✅ **Frontend:**
- Login gọi API ✓
- Signup gọi API ✓
- Checkout step 1 validate đầy đủ ✓
- Checkout step 2 có phương thức thanh toán ✓
- Checkout step 3 tạo order ✓

✅ **Database:**
- Customer được lưu ✓
- Order được lưu ✓
- Order items được lưu ✓
- Payment method được lưu ✓

---

## 🧪 TEST COMMANDS

```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend
cd frontend_demo
python -m http.server 5500

# Database
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d retail_db
SELECT * FROM customers;
SELECT * FROM orders;
```

---

**All changes completed and tested! ✅**
