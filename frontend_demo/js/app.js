// Tech Store Frontend Demo - Backend-integrated (Vanilla JS)
// This frontend is intentionally dependency-free (no bundler) and talks directly to FastAPI.

(function () {
    const DEFAULT_API_BASE = "http://127.0.0.1:8000";
    const STORAGE = {
        apiBase: "api_base",
        token: "customer_token",
        user: "user_profile",
        cart: "cart",
        categories: "categories_cache_v1",
    };

    function _stripTrailingSlashes(url) {
        return String(url || "").replace(/\/+$/, "");
    }

    function getApiBase() {
        return _stripTrailingSlashes(localStorage.getItem(STORAGE.apiBase) || DEFAULT_API_BASE);
    }

    function setApiBase(url) {
        localStorage.setItem(STORAGE.apiBase, _stripTrailingSlashes(url));
    }

    function getToken() {
        return localStorage.getItem(STORAGE.token) || "";
    }

    function setToken(token) {
        localStorage.setItem(STORAGE.token, token || "");
    }

    function clearToken() {
        localStorage.removeItem(STORAGE.token);
    }

    function saveUserProfile(profile) {
        if (!profile) return;
        localStorage.setItem(STORAGE.user, JSON.stringify(profile));
    }

    function getUserProfile() {
        const raw = localStorage.getItem(STORAGE.user);
        if (!raw) return null;
        try {
            return JSON.parse(raw);
        } catch {
            return null;
        }
    }

    function clearUserProfile() {
        localStorage.removeItem(STORAGE.user);
    }

    function _base64UrlDecode(input) {
        const normalized = String(input).replace(/-/g, "+").replace(/_/g, "/");
        const padded = normalized + "===".slice((normalized.length + 3) % 4);
        // atob expects Latin1; JWT payload is JSON ASCII/UTF-8, safe for our usage here.
        return atob(padded);
    }

    function decodeJwtPayload(token) {
        if (!token) return null;
        const parts = String(token).split(".");
        if (parts.length !== 3) return null;
        try {
            return JSON.parse(_base64UrlDecode(parts[1]));
        } catch {
            return null;
        }
    }

    function getCustomerIdFromToken() {
        const payload = decodeJwtPayload(getToken());
        const sub = payload && payload.sub;
        return sub ? String(sub) : null;
    }

    function formatPrice(price) {
        const n = Number(price);
        if (Number.isFinite(n)) return n.toLocaleString("vi-VN") + "đ";
        return String(price ?? "");
    }

    async function apiRequest(path, opts = {}) {
        const {
            method = "GET",
            headers = {},
            json = undefined,
            body = undefined,
            auth = false,
        } = opts;

        const url = String(path).startsWith("http")
            ? String(path)
            : `${getApiBase()}${String(path).startsWith("/") ? "" : "/"}${path}`;

        const h = new Headers(headers);
        if (auth) {
            const token = getToken();
            if (!token) {
                const err = new Error("Unauthorized: missing token");
                err.status = 401;
                throw err;
            }
            h.set("Authorization", `Bearer ${token}`);
        }

        let reqBody = body;
        if (json !== undefined) {
            h.set("Content-Type", "application/json");
            reqBody = JSON.stringify(json);
        }

        const res = await fetch(url, { method, headers: h, body: reqBody });
        const ct = res.headers.get("content-type") || "";
        const isJson = ct.includes("application/json");
        const payload = isJson ? await res.json().catch(() => null) : await res.text().catch(() => "");

        if (!res.ok) {
            const detail =
                (payload && payload.detail) ||
                (payload && payload.error && payload.error.message) ||
                (typeof payload === "string" ? payload : "") ||
                res.statusText;
            const err = new Error(`${res.status} ${detail}`.trim());
            err.status = res.status;
            err.payload = payload;
            throw err;
        }
        return payload;
    }

    // ----- Domain API -----
    async function getCategories({ force = false } = {}) {
        if (!force) {
            const cached = localStorage.getItem(STORAGE.categories);
            if (cached) {
                try {
                    return JSON.parse(cached);
                } catch {
                    // ignore
                }
            }
        }
        const categories = await apiRequest("/categories/?skip=0&limit=100");
        localStorage.setItem(STORAGE.categories, JSON.stringify(categories));
        return categories;
    }

    async function getProducts({ skip = 0, limit = 100 } = {}) {
        return await apiRequest(`/products/?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`);
    }

    async function getProductById(productId) {
        return await apiRequest(`/products/${encodeURIComponent(productId)}`);
    }

    async function getPaymentMethods({ skip = 0, limit = 100 } = {}) {
        return await apiRequest(`/payment-methods/?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`);
    }

    async function createCustomer(payload) {
        return await apiRequest("/customers/", { method: "POST", json: payload });
    }

    async function loginCustomer(payload) {
        // Returns TokenResponse {access_token, token_type}
        return await apiRequest("/customers/login", { method: "POST", json: payload });
    }

    async function getMyProfile() {
        const customerId = getCustomerIdFromToken();
        if (!customerId) {
            const err = new Error("Unauthorized: cannot determine customer_id from token");
            err.status = 401;
            throw err;
        }
        return await apiRequest(`/customers/${encodeURIComponent(customerId)}`, { auth: true });
    }

    async function updateMyProfile(payload) {
        const customerId = getCustomerIdFromToken();
        if (!customerId) {
            const err = new Error("Unauthorized: cannot determine customer_id from token");
            err.status = 401;
            throw err;
        }
        return await apiRequest(`/customers/${encodeURIComponent(customerId)}`, { method: "PUT", auth: true, json: payload });
    }

    async function getMyOrders({ skip = 0, limit = 50 } = {}) {
        return await apiRequest(`/orders/?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`, { auth: true });
    }

    async function createOrder(payload) {
        // payload must include customer_id (must match token sub) + payment_method_id + items[{product_id, quantity}]
        return await apiRequest("/orders/", { method: "POST", auth: true, json: payload });
    }

    async function getAddressesByCustomer(customerId) {
        return await apiRequest(`/addresses/customer/${encodeURIComponent(customerId)}`, { auth: true });
    }

    async function getMyAddresses() {
        const customerId = getCustomerIdFromToken();
        if (!customerId) {
            const err = new Error("Unauthorized: cannot determine customer_id from token");
            err.status = 401;
            throw err;
        }
        return await getAddressesByCustomer(customerId);
    }

    async function createAddress(payload) {
        return await apiRequest("/addresses/", { method: "POST", auth: true, json: payload });
    }

    async function deleteAddress(addressId) {
        return await apiRequest(`/addresses/${encodeURIComponent(addressId)}`, { method: "DELETE", auth: true });
    }

    async function getWishlistByCustomer(customerId) {
        return await apiRequest(`/wishlists/customer/${encodeURIComponent(customerId)}`, { auth: true });
    }

    async function getMyWishlist() {
        const customerId = getCustomerIdFromToken();
        if (!customerId) {
            const err = new Error("Unauthorized: cannot determine customer_id from token");
            err.status = 401;
            throw err;
        }
        return await getWishlistByCustomer(customerId);
    }

    async function addWishlistItem(productId) {
        const customerId = getCustomerIdFromToken();
        if (!customerId) {
            const err = new Error("Unauthorized: cannot determine customer_id from token");
            err.status = 401;
            throw err;
        }
        return await apiRequest("/wishlists/", { method: "POST", auth: true, json: { customer_id: customerId, product_id: String(productId) } });
    }

    async function removeWishlistItem(wishlistId) {
        return await apiRequest(`/wishlists/${encodeURIComponent(wishlistId)}`, { method: "DELETE", auth: true });
    }

    async function getReviewsByProduct(productId) {
        return await apiRequest(`/reviews/product/${encodeURIComponent(productId)}`);
    }

    async function createReview(payload) {
        return await apiRequest("/reviews/", { method: "POST", auth: true, json: payload });
    }

    // ----- Cart (LocalStorage) -----
    function getCart() {
        return JSON.parse(localStorage.getItem(STORAGE.cart) || "[]");
    }

    function saveCart(cart) {
        localStorage.setItem(STORAGE.cart, JSON.stringify(cart || []));
        updateCartCount();
    }

    function addToCart(product, quantity = 1) {
        const cart = getCart();
        const productId = String(product.product_id);
        const existing = cart.find((i) => String(i.product_id) === productId);
        if (existing) existing.quantity += quantity;
        else {
            cart.push({
                product_id: productId,
                product_name: product.product_name,
                unit_price: Number(product.unit_price),
                category_id: String(product.category_id),
                quantity,
            });
        }
        saveCart(cart);
    }

    function removeFromCartByIndex(index) {
        const cart = getCart();
        cart.splice(index, 1);
        saveCart(cart);
    }

    function updateCartQuantity(index, quantity) {
        const cart = getCart();
        if (!cart[index]) return;
        if (quantity <= 0) cart.splice(index, 1);
        else cart[index].quantity = quantity;
        saveCart(cart);
    }

    function updateCartCount() {
        const cart = getCart();
        const count = cart.reduce((sum, i) => sum + (Number(i.quantity) || 0), 0);
        document.querySelectorAll(".cart-count").forEach((el) => (el.textContent = String(count)));
    }

    function clearCart() {
        localStorage.removeItem(STORAGE.cart);
        updateCartCount();
    }

    function pickCategoryIcon(name) {
        const s = String(name || "").toLowerCase();
        if (s.includes("phone")) return "📱";
        if (s.includes("laptop") || s.includes("computer") || s.includes("pc")) return "💻";
        if (s.includes("access")) return "🎧";
        if (s.includes("watch") || s.includes("wear")) return "⌚";
        return "🛍️";
    }

    async function categoryNameById(categoryId) {
        const cats = await getCategories();
        const found = (cats || []).find((c) => String(c.category_id) === String(categoryId));
        return found ? found.category_name : String(categoryId);
    }

    function requireLoginOrRedirect() {
        if (!getToken()) {
            window.location.href = "customer-login.html";
            return false;
        }
        return true;
    }

    // Export
    window.app = {
        // config/auth
        getApiBase,
        setApiBase,
        getToken,
        setToken,
        clearToken,
        decodeJwtPayload,
        getCustomerIdFromToken,
        saveUserProfile,
        getUserProfile,
        clearUserProfile,
        requireLoginOrRedirect,

        // api
        apiRequest,
        getCategories,
        getProducts,
        getProductById,
        getPaymentMethods,
        createCustomer,
        loginCustomer,
        getMyProfile,
        updateMyProfile,
        getMyOrders,
        createOrder,
        getMyAddresses,
        createAddress,
        deleteAddress,
        getMyWishlist,
        addWishlistItem,
        removeWishlistItem,
        getReviewsByProduct,
        createReview,

        // helpers
        formatPrice,
        categoryNameById,
        pickCategoryIcon,

        // cart
        getCart,
        saveCart,
        addToCart,
        removeFromCartByIndex,
        updateCartQuantity,
        updateCartCount,
        clearCart,
    };

    // init cart count
    document.addEventListener("DOMContentLoaded", updateCartCount);
})();

