(function () {
  var DEFAULT_IMAGE = (window.TamTai && TamTai.DEFAULT_PRODUCT_IMAGE) || "../../images/acer-refurbished-laptop-500x500.webp";

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function normalizeText(value) {
    if (window.TamTai && typeof TamTai.normalizeText === "function") {
      return TamTai.normalizeText(value);
    }

    return String(value || "")
      .trim()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function getShippingFee() {
    var checked = document.querySelector('input[name="shipping"]:checked');
    if (!checked) {
      return 0;
    }
    var wrapper = checked.closest(".method-item");
    if (!wrapper) {
      return 0;
    }
    var amountEl = wrapper.querySelector("strong");
    return amountEl ? TamTai.parseCurrency(amountEl.textContent) : 0;
  }

  function getShippingMethodLabel() {
    var checked = document.querySelector('input[name="shipping"]:checked');
    if (!checked) {
      return "";
    }
    var wrapper = checked.closest(".method-item");
    var text = wrapper ? wrapper.querySelector("span") : null;
    return text ? String(text.textContent || "").trim() : "";
  }

  function getPaymentMethodLabel() {
    var checked = document.querySelector('input[name="payment"]:checked');
    if (!checked) {
      return "";
    }
    var wrapper = checked.closest(".method-item");
    var text = wrapper ? wrapper.querySelector("span") : null;
    return text ? String(text.textContent || "").trim() : "";
  }

  function ensureSummaryContainer() {
    var orderSummary = document.querySelector(".order-summary");
    if (!orderSummary) {
      return null;
    }

    var listWrap = orderSummary.querySelector("#checkoutSummaryItems");
    if (listWrap) {
      return listWrap;
    }

    listWrap = document.createElement("div");
    listWrap.id = "checkoutSummaryItems";
    var firstSummaryItem = orderSummary.querySelector(".summary-item");
    if (firstSummaryItem) {
      orderSummary.querySelectorAll(".summary-item").forEach(function (item) {
        listWrap.appendChild(item);
      });
      orderSummary.insertBefore(listWrap, orderSummary.querySelector(".price-line"));
    }
    return listWrap;
  }

  function toImageSrc(imageUrl) {
    var raw = String(imageUrl || "").trim();
    if (!raw) {
      return DEFAULT_IMAGE;
    }

    if (/^https?:\/\//i.test(raw) || raw.startsWith("data:")) {
      return raw;
    }

    if (window.TamTai && typeof TamTai.buildApiUrl === "function") {
      if (raw.startsWith("/")) {
        return TamTai.buildApiUrl(raw);
      }
      return TamTai.buildApiUrl("/" + raw);
    }

    return raw;
  }

  function renderSummaryItems() {
    var cart = TamTai.getCart();
    var listWrap = ensureSummaryContainer();
    if (!listWrap) {
      return { subtotal: 0, total: 0 };
    }

    if (!cart.length) {
      listWrap.innerHTML = '<p class="empty-cart-note">Gi\u1ecf h\u00e0ng \u0111ang tr\u1ed1ng.</p>';
    } else {
      listWrap.innerHTML = cart.map(function (item) {
        var image = toImageSrc(item.image);
        var name = String(item.name || "S\u1ea3n ph\u1ea9m");
        var qty = Math.max(1, Number(item.qty || 1));
        var price = Number(item.price || 0);

        return [
          '<div class="summary-item">',
          '  <div class="thumb"><img src="' + escapeHtml(image) + '" alt="' + escapeHtml(name) + '"></div>',
          '  <div class="meta">',
          "    <h3>" + escapeHtml(name) + "</h3>",
          "    <p>SL: " + qty + "</p>",
          "  </div>",
          "  <strong>" + TamTai.formatCurrency(price * qty) + "</strong>",
          "</div>"
        ].join("");
      }).join("");
    }

    var subtotal = cart.reduce(function (sum, item) {
      return sum + Number(item.price || 0) * Math.max(1, Number(item.qty || 1));
    }, 0);
    var shippingFee = getShippingFee();
    var total = subtotal + shippingFee;

    var lines = document.querySelectorAll(".order-summary .price-line");
    if (lines[0]) {
      lines[0].querySelector("strong").textContent = TamTai.formatCurrency(subtotal);
    }
    if (lines[1]) {
      lines[1].querySelector("strong").textContent = TamTai.formatCurrency(shippingFee);
    }
    if (lines[2]) {
      lines[2].querySelector("strong").textContent = TamTai.formatCurrency(total);
    }

    return { subtotal: subtotal, total: total };
  }

  function getCheckoutFields() {
    var checkoutForm = document.querySelector(".checkout-form");
    var textInputs = checkoutForm ? checkoutForm.querySelectorAll('input[type="text"]') : [];

    var fullNameInput = textInputs.length > 0 ? textInputs[0] : null;
    var detailAddressInput = textInputs.length > 1 ? textInputs[textInputs.length - 1] : null;
    var phoneInput = checkoutForm ? checkoutForm.querySelector('input[type="tel"]') : null;
    var emailInput = checkoutForm ? checkoutForm.querySelector('input[type="email"]') : null;
    var citySelect = checkoutForm ? checkoutForm.querySelector("select") : null;
    var noteTextarea = checkoutForm ? checkoutForm.querySelector("textarea") : null;

    var cityValue = citySelect ? String(citySelect.value || "").trim() : "";
    if (normalizeText(cityValue).indexOf("chon tinh") !== -1) {
      cityValue = "";
    }

    return {
      fullName: fullNameInput ? String(fullNameInput.value || "").trim() : "",
      phone: phoneInput ? String(phoneInput.value || "").trim() : "",
      email: emailInput ? String(emailInput.value || "").trim() : "",
      city: cityValue,
      detailAddress: detailAddressInput ? String(detailAddressInput.value || "").trim() : "",
      note: noteTextarea ? String(noteTextarea.value || "").trim() : ""
    };
  }

  function validateCheckoutFields(fields) {
    if (!fields.fullName || !fields.phone || !fields.email || !fields.city || !fields.detailAddress) {
      return { ok: false, message: "Vui l\u00f2ng \u0111i\u1ec1n \u0111\u1ea7y \u0111\u1ee7 th\u00f4ng tin giao h\u00e0ng." };
    }

    if (fields.email.indexOf("@") === -1) {
      return { ok: false, message: "Email kh\u00f4ng h\u1ee3p l\u1ec7." };
    }

    var paymentChecked = document.querySelector('input[name="payment"]:checked');
    if (!paymentChecked) {
      return { ok: false, message: "Vui l\u00f2ng ch\u1ecdn ph\u01b0\u01a1ng th\u1ee9c thanh to\u00e1n." };
    }

    return { ok: true };
  }

  function composeShippingAddress(fields) {
    var parts = [
      "Nguoi nhan: " + fields.fullName,
      "SDT: " + fields.phone,
      "Email: " + fields.email,
      "Khu vuc: " + fields.city,
      "Dia chi: " + fields.detailAddress
    ];

    var shippingMethod = getShippingMethodLabel();
    if (shippingMethod) {
      parts.push("Van chuyen: " + shippingMethod);
    }

    if (fields.note) {
      parts.push("Ghi chu: " + fields.note);
    }

    return parts.join(" | ");
  }

  async function resolveCurrentCustomerId(token) {
    var fromStorage = String(localStorage.getItem("tamtai_customer_id") || "").trim();
    if (fromStorage) {
      return fromStorage;
    }

    var profileRaw = localStorage.getItem("tamtai_customer_profile");
    if (profileRaw) {
      try {
        var profile = JSON.parse(profileRaw);
        if (profile && profile.customer_id) {
          var profileId = String(profile.customer_id).trim();
          if (profileId) {
            localStorage.setItem("tamtai_customer_id", profileId);
            return profileId;
          }
        }
      } catch (error) {
        // ignore malformed cached profile
      }
    }

    var me = await TamTai.fetchJson("/customers/me", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token
      }
    });

    var customerId = String((me && me.customer_id) || "").trim();
    if (!customerId) {
      throw new Error("Kh\u00f4ng x\u00e1c \u0111\u1ecbnh \u0111\u01b0\u1ee3c t\u00e0i kho\u1ea3n \u0111ang nh\u1eadp.");
    }

    localStorage.setItem("tamtai_customer_id", customerId);
    return customerId;
  }

  function pickPaymentMethod(methods, selectedLabel) {
    if (!Array.isArray(methods) || !methods.length) {
      return null;
    }

    var selected = normalizeText(selectedLabel);

    function includesAny(haystack, keywords) {
      return keywords.some(function (keyword) {
        return haystack.indexOf(keyword) !== -1;
      });
    }

    var normalizedMethods = methods.map(function (method) {
      return {
        raw: method,
        normalizedName: normalizeText(method.mode_name)
      };
    });

    var keywordSets = {
      cod: ["cod", "nhan hang", "tien mat", "cash"],
      bank: ["chuyen khoan", "ngan hang", "bank"],
      wallet: ["vi", "momo", "zalopay", "wallet"]
    };

    var targetGroup = "";
    if (includesAny(selected, keywordSets.cod)) {
      targetGroup = "cod";
    } else if (includesAny(selected, keywordSets.bank)) {
      targetGroup = "bank";
    } else if (includesAny(selected, keywordSets.wallet)) {
      targetGroup = "wallet";
    }

    if (targetGroup) {
      var foundByGroup = normalizedMethods.find(function (entry) {
        return includesAny(entry.normalizedName, keywordSets[targetGroup]);
      });
      if (foundByGroup) {
        return foundByGroup.raw;
      }
    }

    var foundByExact = normalizedMethods.find(function (entry) {
      return entry.normalizedName === selected;
    });
    if (foundByExact) {
      return foundByExact.raw;
    }

    return methods[0];
  }

  function buildOrderItemsFromCart(cart) {
    return cart.map(function (item) {
      var productId = String(item.productId || item.id || "").trim();
      return {
        product_id: productId,
        quantity: Math.max(1, Number(item.qty || 1))
      };
    }).filter(function (item) {
      return Boolean(item.product_id);
    });
  }

  async function submitCheckout(confirmBtn) {
    var token = localStorage.getItem("access_token");
    if (!token || TamTai.getRole() !== "user") {
      window.location.href = "../auth/login.html?redirect=" + encodeURIComponent("../cart/checkout.html");
      return;
    }

    var cart = TamTai.getCart();
    if (!Array.isArray(cart) || !cart.length) {
      alert("Gi\u1ecf h\u00e0ng \u0111ang tr\u1ed1ng, kh\u00f4ng th\u1ec3 x\u00e1c nh\u1eadn thanh to\u00e1n.");
      return;
    }

    var fields = getCheckoutFields();
    var validation = validateCheckoutFields(fields);
    if (!validation.ok) {
      alert(validation.message);
      return;
    }

    var paymentLabel = getPaymentMethodLabel();

    confirmBtn.disabled = true;
    var originalText = confirmBtn.textContent;
    confirmBtn.textContent = "Dang xu ly...";

    try {
      var customerId = await resolveCurrentCustomerId(token);
      var paymentMethods = await TamTai.fetchJson("/payment-methods?skip=0&limit=100");
      var selectedPayment = pickPaymentMethod(paymentMethods, paymentLabel);

      if (!selectedPayment || !selectedPayment.payment_method_id) {
        throw new Error("Ch\u01b0a c\u00f3 ph\u01b0\u01a1ng th\u1ee9c thanh to\u00e1n trong h\u1ec7 th\u1ed1ng.");
      }

      var orderItems = buildOrderItemsFromCart(cart);
      if (!orderItems.length) {
        throw new Error("Kh\u00f4ng c\u00f3 s\u1ea3n ph\u1ea9m h\u1ee3p l\u1ec7 \u0111\u1ec3 t\u1ea1o \u0111\u01a1n h\u00e0ng.");
      }

      var payload = {
        customer_id: customerId,
        payment_method_id: String(selectedPayment.payment_method_id),
        shipping_address: composeShippingAddress(fields),
        shipping_fee: getShippingFee(),
        discount_amount: 0,
        items: orderItems
      };

      var order = await TamTai.fetchJson("/orders/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token
        },
        body: JSON.stringify(payload)
      });

      TamTai.clearCart();
      alert("Dat hang thanh cong. Ma don: #" + String(order.order_id || ""));

      if (order && order.order_id) {
        window.location.href = "order-detail.html?id=" + encodeURIComponent(String(order.order_id));
      } else {
        window.location.href = "all-orders.html";
      }
    } catch (error) {
      alert("Khong the tao don hang: " + (error && error.message ? error.message : "Loi khong xac dinh"));
    } finally {
      confirmBtn.disabled = false;
      confirmBtn.textContent = originalText;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    TamTai.setupSearchRedirect(".search-box input", "../products/products.html");

    renderSummaryItems();

    document.querySelectorAll('input[name="shipping"]').forEach(function (radio) {
      radio.addEventListener("change", renderSummaryItems);
    });

    var confirmBtn = document.querySelector(".confirm-btn");
    if (confirmBtn) {
      confirmBtn.addEventListener("click", function () {
        submitCheckout(confirmBtn);
      });
    }
  });
})();
