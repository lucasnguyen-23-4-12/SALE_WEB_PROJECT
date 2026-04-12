(function () {
  var CART_KEY = "tamtai_cart";
  var PROFILE_KEY = "tamtai_profile";
  var API_BASE_URL = "http://127.0.0.1:8000";
  var GOOGLE_CLIENT_ID = "27435447565-fk6hsgmd17rqjuqegeqvq1monbo632gr.apps.googleusercontent.com";
  var DEFAULT_PRODUCT_IMAGE = "../../images/acer-refurbished-laptop-500x500.webp";

  function parseJson(raw, fallback) {
    try {
      return JSON.parse(raw);
    } catch (error) {
      return fallback;
    }
  }


  function sanitizeStorageKeyPart(value, fallback) {
    var raw = String(value || "").trim();
    if (!raw) {
      return fallback || "unknown";
    }

    var safe = raw.replace(/[^a-zA-Z0-9_-]/g, "_");
    return safe || (fallback || "unknown");
  }

  function parseJwtPayload(token) {
    if (!token || typeof token !== "string") {
      return null;
    }

    var parts = token.split(".");
    if (parts.length < 2) {
      return null;
    }

    try {
      var payload = parts[1].replace(/-/g, "+").replace(/_/g, "/");
      while (payload.length % 4 !== 0) {
        payload += "=";
      }

      if (typeof atob !== "function") {
        return null;
      }

      return JSON.parse(atob(payload));
    } catch (error) {
      return null;
    }
  }

  function getCartStorageKey() {
    var role = localStorage.getItem("tamtai_role") || "guest";

    if (role !== "user") {
      return CART_KEY;
    }

    var customerId = localStorage.getItem("tamtai_customer_id");
    if (customerId) {
      return CART_KEY + "_user_" + sanitizeStorageKeyPart(customerId, "unknown");
    }

    var profile = parseJson(localStorage.getItem("tamtai_customer_profile"), null);
    if (profile && profile.customer_id) {
      return CART_KEY + "_user_" + sanitizeStorageKeyPart(profile.customer_id, "unknown");
    }

    var token = localStorage.getItem("access_token");
    var payload = parseJwtPayload(token);
    var tokenUserId = payload && (payload.sub || payload.customer_id || payload.user_id || payload.email);
    if (tokenUserId) {
      return CART_KEY + "_user_" + sanitizeStorageKeyPart(tokenUserId, "unknown");
    }

    return CART_KEY + "_user_anonymous";
  }

  function normalizeCart(rawCart) {
    if (Array.isArray(rawCart)) {
      return rawCart;
    }

    if (rawCart && Array.isArray(rawCart.items)) {
      return rawCart.items;
    }

    return [];
  }

  function getCart() {
    return normalizeCart(parseJson(localStorage.getItem(getCartStorageKey()), []));
  }

  function saveCart(cart) {
    var normalizedCart = normalizeCart(cart);
    localStorage.setItem(getCartStorageKey(), JSON.stringify(normalizedCart));
    window.dispatchEvent(new CustomEvent("tamtai:cart-updated", { detail: { cart: normalizedCart } }));
  }

  function addToCart(item, quantity) {
    var qty = Number(quantity || 1);
    if (qty < 1) {
      qty = 1;
    }

    var productId = item && (item.productId || item.id) ? String(item.productId || item.id) : "item-" + Date.now();
    var cart = getCart();
    var existing = cart.find(function (entry) {
      return String(entry.productId || entry.id) === productId;
    });

    if (existing) {
      existing.qty += qty;
    } else {
      cart.push({
        id: productId,
        productId: productId,
        categoryId: item && item.categoryId ? String(item.categoryId) : null,
        name: item && item.name ? item.name : "S\u1ea3n ph\u1ea9m",
        price: Number((item && item.price) || 0),
        oldPrice: Number((item && (item.oldPrice || item.price)) || 0),
        image: item && item.image ? item.image : DEFAULT_PRODUCT_IMAGE,
        qty: qty
      });
    }

    saveCart(cart);
  }

  function clearCart() {
    saveCart([]);
  }

  function formatCurrency(value) {
    return Number(value || 0).toLocaleString("vi-VN") + "\u20ab";
  }

  function parseCurrency(text) {
    if (!text) {
      return 0;
    }

    var numeric = String(text).replace(/[^\d]/g, "");
    return Number(numeric || 0);
  }

  function normalizeText(value) {
    if (value === null || value === undefined) {
      return "";
    }

    return String(value)
      .trim()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function buildApiUrl(path) {
    var input = String(path || "");
    if (/^https?:\/\//i.test(input)) {
      return input;
    }

    if (!input.startsWith("/")) {
      input = "/" + input;
    }

    return API_BASE_URL + input;
  }

  async function fetchJson(path, options) {
    var response = await fetch(buildApiUrl(path), options || {});
    var body = null;

    try {
      body = await response.json();
    } catch (error) {
      body = null;
    }

    if (!response.ok) {
      var message = body && body.detail ? body.detail : ("Request failed: " + response.status);
      throw new Error(String(message));
    }

    return body;
  }

  function getRole() {
    return localStorage.getItem("tamtai_role") || "guest";
  }

  function showAdminMenuLink(rootNode) {
    var root = rootNode || document;
    var adminMenuLink = root.querySelector("#adminMenuLink");
    if (!adminMenuLink) {
      return;
    }
    adminMenuLink.style.display = getRole() === "admin" ? "flex" : "none";
  }

  function setupSearchRedirect(inputSelector, redirectPath) {
    var input = typeof inputSelector === "string" ? document.querySelector(inputSelector) : inputSelector;
    if (!input) {
      return;
    }

    input.addEventListener("keydown", function (event) {
      if (event.key !== "Enter") {
        return;
      }

      var keyword = input.value.trim();
      if (!keyword) {
        return;
      }

      var destination = redirectPath || "../products/products.html";
      window.location.href = destination + "?q=" + encodeURIComponent(keyword);
    });
  }

  function getProfile() {
    return parseJson(localStorage.getItem(PROFILE_KEY), {
      fullName: "",
      email: "",
      phone: "",
      address: ""
    });
  }

  function saveProfile(profile) {
    localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
  }

  function clearSession() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");
    localStorage.removeItem("tamtai_role");
    localStorage.removeItem("tamtai_customer_id");
    localStorage.removeItem("tamtai_customer_profile");
    localStorage.removeItem(PROFILE_KEY);
  }

  function logout(redirectPath) {
    clearSession();
    window.location.href = redirectPath || "../auth/login.html";
  }

  function bindLogoutButtons(rootNode) {
    var root = rootNode || document;
    var buttons = root.querySelectorAll("[data-logout]");
    if (!buttons.length) {
      return;
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function (event) {
        event.preventDefault();
        logout(button.getAttribute("data-redirect") || "../auth/login.html");
      });
    });
  }

  window.TamTai = {
    API_BASE_URL: API_BASE_URL,
    GOOGLE_CLIENT_ID: GOOGLE_CLIENT_ID,
    DEFAULT_PRODUCT_IMAGE: DEFAULT_PRODUCT_IMAGE,
    getCart: getCart,
    saveCart: saveCart,
    addToCart: addToCart,
    clearCart: clearCart,
    formatCurrency: formatCurrency,
    parseCurrency: parseCurrency,
    normalizeText: normalizeText,
    buildApiUrl: buildApiUrl,
    fetchJson: fetchJson,
    getRole: getRole,
    showAdminMenuLink: showAdminMenuLink,
    setupSearchRedirect: setupSearchRedirect,
    getProfile: getProfile,
    saveProfile: saveProfile,
    clearSession: clearSession,
    logout: logout,
    bindLogoutButtons: bindLogoutButtons
  };

  document.addEventListener("DOMContentLoaded", function () {
    showAdminMenuLink(document);
    bindLogoutButtons(document);
  });
})();

