// Mock Products Data (backend schema names)
// URL của backend đang chạy
const API_BASE = 'http://127.0.0.1:8000';

async function fetchProducts(skip = 0, limit = 12) {
    const res = await fetch(`${API_BASE}/products?skip=${skip}&limit=${limit}`);
    if (!res.ok) throw new Error('Fetch products failed');
    return res.json();
}

async function fetchProductById(id) {
    const res = await fetch(`${API_BASE}/products/${id}`);
    if (!res.ok) throw new Error('Fetch product failed');
    return res.json();
}

async function createOrderOnServer(orderPayload) {
    const res = await fetch(`${API_BASE}/orders/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderPayload)
    });
    if (!res.ok) throw new Error('Create order failed');
    return res.json();
}

async function createCustomer(customerData) {
    const res = await fetch(`${API_BASE}/customers/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customerData)
    });
    if (!res.ok) throw new Error('Create customer failed');
    return res.json();
}

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

const mockProducts = [
    {
        product_id: 1,
        product_name: 'iPhone 15 Pro Max',
        category_id: 10,
        category_name: 'smartphones',
        unit_price: 28000000,
        original_price: 35000000,
        discount_percent: 20,
        rating_avg: 4.8,
        total_reviews: 245,
        stock_quantity: 25,
        description: 'Điện thoại flagship Apple với chip A17 Pro, camera tele 5x, và màn hình Super Retina XDR.',
        image_url: ''
    },
    {
        product_id: 2,
        product_name: 'Samsung Galaxy S24 Ultra',
        category_id: 10,
        category_name: 'smartphones',
        unit_price: 26000000,
        original_price: 33000000,
        discount_percent: 21,
        rating_avg: 4.7,
        total_reviews: 198,
        stock_quantity: 18,
        description: 'Điện thoại Android với bút S Pen tích hợp, camera 200MP, và pin dung lượng lớn.',
        image_url: ''
    },
    {
        product_id: 3,
        product_name: 'MacBook Pro 16"',
        category_id: 20,
        category_name: 'computers',
        unit_price: 45000000,
        original_price: 56000000,
        discount_percent: 20,
        rating_avg: 4.9,
        total_reviews: 156,
        stock_quantity: 8,
        description: 'Laptop Apple mạnh mẽ với chip M3 Max, 18GB RAM, và màn hình Retina 3456x2234.',
        image_url: ''
    },
    {
        product_id: 4,
        product_name: 'Dell XPS 15',
        category_id: 20,
        category_name: 'computers',
        unit_price: 35000000,
        original_price: 42000000,
        discount_percent: 17,
        rating_avg: 4.6,
        total_reviews: 132,
        stock_quantity: 12,
        description: 'Laptop Windows cao cấp với Intel Core Ultra, RTX 4050, và màn hình OLED 3.5K.',
        image_url: ''
    },
    {
        product_id: 5,
        product_name: 'AirPods Pro 2',
        category_id: 30,
        category_name: 'accessories',
        unit_price: 6500000,
        original_price: 8000000,
        discount_percent: 19,
        rating_avg: 4.8,
        total_reviews: 512,
        stock_quantity: 60,
        description: 'Tai nghe không dây Apple với chống ồn chủ động và âm thanh không gian.',
        image_url: ''
    },
    {
        product_id: 6,
        product_name: 'Sony WH-1000XM5',
        category_id: 30,
        category_name: 'accessories',
        unit_price: 7200000,
        original_price: 9000000,
        discount_percent: 20,
        rating_avg: 4.7,
        total_reviews: 445,
        stock_quantity: 40,
        description: 'Tai nghe over-ear premium với chống ồn tốt nhất trong tầm giá.',
        image_url: ''
    },
    {
        product_id: 7,
        product_name: 'Apple Watch Series 9',
        category_id: 40,
        category_name: 'wearables',
        unit_price: 12000000,
        original_price: 15000000,
        discount_percent: 20,
        rating_avg: 4.7,
        total_reviews: 367,
        stock_quantity: 30,
        description: 'Smartwatch Apple với màn hình Always-On, đo ECG, và pin 18 giờ.',
        image_url: ''
    },
    {
        product_id: 8,
        product_name: 'Google Pixel Watch 2',
        category_id: 40,
        category_name: 'wearables',
        unit_price: 9500000,
        original_price: 11800000,
        discount_percent: 19,
        rating_avg: 4.5,
        total_reviews: 228,
        stock_quantity: 22,
        description: 'Smartwatch Android với chip Snapdragon, pin 24 giờ, và màn hình AMOLED.',
        image_url: ''
    },
    {
        product_id: 9,
        product_name: 'iPad Pro 12.9"',
        category_id: 20,
        category_name: 'computers',
        unit_price: 32000000,
        original_price: 40000000,
        discount_percent: 20,
        rating_avg: 4.8,
        total_reviews: 289,
        stock_quantity: 14,
        description: 'Tablet Apple cao cấp với M2, màn hình Liquid Retina XDR, và hỗ trợ Apple Pencil Pro.',
        image_url: ''
    },
    {
        product_id: 10,
        product_name: 'USB-C Fast Charger 65W',
        category_id: 30,
        category_name: 'accessories',
        unit_price: 1200000,
        original_price: 1500000,
        discount_percent: 20,
        rating_avg: 4.6,
        total_reviews: 890,
        stock_quantity: 200,
        description: 'Sạc nhanh USB-C tiêu chuẩn PD, tương thích với hầu hết thiết bị.',
        image_url: ''
    },
    {
        product_id: 11,
        product_name: 'Asus ROG Laptop',
        category_id: 20,
        category_name: 'computers',
        unit_price: 40000000,
        original_price: 50000000,
        discount_percent: 20,
        rating_avg: 4.7,
        total_reviews: 178,
        stock_quantity: 6,
        description: 'Laptop gaming với RTX 4090, chip Intel i9, và tấn nhiệt hơn 500W.',
        image_url: ''
    },
    {
        product_id: 12,
        product_name: 'OnePlus 12',
        category_id: 10,
        category_name: 'smartphones',
        unit_price: 16000000,
        original_price: 20000000,
        discount_percent: 20,
        rating_avg: 4.6,
        total_reviews: 267,
        stock_quantity: 28,
        description: 'Smartphone flagship killer với Snapdragon 8 Gen 3, sạc 100W, và camera ổn định.',
        image_url: ''
    }
];

// NOTE: frontend uses backend-style field names above. Display helpers below map to those fields.

// Cart Management
function getCart() {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
}

function addToCart(product, quantity = 1) {
    let cart = getCart();
    const existingItem = cart.find(item => item.product_id === product.product_id);

    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            product_id: product.product_id,
            product_name: product.product_name,
            category_id: product.category_id,
            category_name: product.category_name,
            unit_price: product.unit_price,
            quantity: quantity
        });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const cart = getCart();
    const total = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(el => {
        el.textContent = total;
        if (total > 0) {
            el.style.display = 'inline-block';
        } else {
            el.style.display = 'none';
        }
    });
}

// Initialize cart count on page load
document.addEventListener('DOMContentLoaded', updateCartCount);

// Search Function
function searchProducts(query) {
    const searchQuery = query.toLowerCase();
    return mockProducts.filter(product =>
        product.product_name.toLowerCase().includes(searchQuery) ||
        product.category_name.toLowerCase().includes(searchQuery) ||
        (product.description || '').toLowerCase().includes(searchQuery)
    );
}

// Filter by Category
function filterByCategory(category) {
    // category may be id or name
    return mockProducts.filter(product => product.category_id === category || product.category_name === category);
}

// Filter by Price Range
function filterByPrice(minPrice, maxPrice) {
    return mockProducts.filter(product => product.unit_price >= minPrice && product.unit_price <= maxPrice);
}

// Filter by Rating
function filterByRating(minRating) {
    return mockProducts.filter(product => product.rating_avg >= minRating);
}

// Sort Products
function sortProducts(products, sortBy) {
    let sorted = [...products];

    switch(sortBy) {
        case 'price-low':
            sorted.sort((a, b) => a.unit_price - b.unit_price);
            break;
        case 'price-high':
            sorted.sort((a, b) => b.unit_price - a.unit_price);
            break;
        case 'rating':
            sorted.sort((a, b) => b.rating_avg - a.rating_avg);
            break;
        case 'newest':
            sorted.sort((a, b) => b.product_id - a.product_id);
            break;
        case 'reviews':
            sorted.sort((a, b) => b.total_reviews - a.total_reviews);
            break;
        default:
            return products;
    }

    return sorted;
}

// Get Product by ID
function getProductById(id) {
    return mockProducts.find(product => product.product_id === id);
}

// Get Related Products
function getRelatedProducts(productId, limit = 4) {
    const product = getProductById(productId);
    if (!product) return [];

    return mockProducts
        .filter(p => p.category_id === product.category_id && p.product_id !== productId)
        .slice(0, limit);
}

// Get Featured Products
function getFeaturedProducts(limit = 4) {
    return sortProducts(mockProducts, 'rating').slice(0, limit);
}

// Get New Products
function getNewProducts(limit = 4) {
    return sortProducts(mockProducts, 'newest').slice(0, limit);
}

// Price Formatting
function formatPrice(price) {
    return price.toLocaleString('vi-VN') + 'đ';
}

// Customer Management
function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function saveUserProfile(userData) {
    localStorage.setItem('user', JSON.stringify(userData));
}

// Order Management
function createOrder(orderData) {
    const orders = JSON.parse(localStorage.getItem('orders')) || [];
    const order_id = 'ĐH-' + Math.floor(Math.random() * 1000000);
    const order = {
        order_id,
        customer_id: orderData.customer_id || null,
        payment_method_id: orderData.payment_method_id || null,
        order_date: new Date().toISOString(),
        status: 'pending',
        shipping_address: orderData.shipping_address || null,
        shipping_fee: orderData.shipping_fee || 0,
        discount_amount: orderData.discount_amount || 0,
        items: (orderData.items || []).map((it, idx) => ({
            order_item_id: 'OI-' + Math.floor(Math.random() * 1000000) + '-' + idx,
            order_id,
            product_id: it.product_id,
            quantity: it.quantity,
            price_at_purchase: it.price_at_purchase || it.unit_price || 0,
            amount: (it.quantity * (it.price_at_purchase || it.unit_price || 0)),
            profit: 0,
            discount: it.discount || 0
        }))
    };

    orders.push(order);
    localStorage.setItem('orders', JSON.stringify(orders));
    return order;
}

function getOrders() {
    return JSON.parse(localStorage.getItem('orders')) || [];
}

function getOrderById(orderId) {
    const orders = getOrders();
    return orders.find(order => order.id === orderId);
}

// Validation Functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone.replace(/[^0-9]/g, ''));
}

function isValidPassword(password) {
    return password.length >= 6;
}

// Utility Functions
function generateOrderNumber() {
    return 'ĐH-' + new Date().getTime();
}

function calculateOrderTotal(items, shipping = 0) {
    const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    return subtotal + shipping;
}

function calculateDiscount(originalPrice, salePrice) {
    return Math.round(((originalPrice - salePrice) / originalPrice) * 100);
}

// Notification System
function showNotification(message, type = 'success') {
    // Simple notification (can be replaced with a more sophisticated system)
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Shopping Analytics
function trackProductView(productId) {
    const viewed = JSON.parse(localStorage.getItem('viewed_products')) || [];
    if (!viewed.includes(productId)) {
        viewed.push(productId);
    }
    localStorage.setItem('viewed_products', JSON.stringify(viewed));
}

function getViewedProducts() {
    return JSON.parse(localStorage.getItem('viewed_products')) || [];
}

// Wishlist Management
function addToWishlist(productId) {
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    if (!wishlist.includes(productId)) {
        wishlist.push(productId);
    }
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
}

function removeFromWishlist(productId) {
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    wishlist = wishlist.filter(id => id !== productId);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
}

function getWishlist() {
    return JSON.parse(localStorage.getItem('wishlist')) || [];
}

function isInWishlist(productId) {
    return getWishlist().includes(productId);
}

// Export functions for use in HTML pages
window.app = {
    mockProducts,
    getCart,
    addToCart,
    updateCartCount,
    searchProducts,
    filterByCategory,
    filterByPrice,
    filterByRating,
    sortProducts,
    getProductById,
    getRelatedProducts,
    getFeaturedProducts,
    getNewProducts,
    formatPrice,
    getCurrentUser,
    saveUserProfile,
    createOrder,
    getOrders,
    getOrderById,
    isValidEmail,
    isValidPhone,
    isValidPassword,
    generateOrderNumber,
    calculateOrderTotal,
    calculateDiscount,
    showNotification,
    trackProductView,
    getViewedProducts,
    addToWishlist,
    removeFromWishlist,
    getWishlist,
    isInWishlist,
    // network-aware helpers
    fetchProducts,
    fetchProductById,
    createOrderOnServer,
    loadProductList,
    loadProduct,
    submitOrder,
    createCustomer,
    loginCustomer,
    createPaymentMethod
};

// Log initial state
console.log('Tech Store Frontend Loaded Successfully!');
console.log('Mock Products:', mockProducts.length);
console.log('Cart Items:', getCart().length);
