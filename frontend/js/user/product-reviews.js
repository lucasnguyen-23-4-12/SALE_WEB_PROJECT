(function () {
  var state = {
    token: "",
    customerId: "",
    products: [],
    reviewsByProduct: {}
  };

  var DEFAULT_IMAGE = "../../images/acer-refurbished-laptop-500x500.webp";

  function displayValue(value) {
    var text = (value || "").toString().trim();
    return text ? text : "chưa có";
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function formatDate(dateValue) {
    if (!dateValue) {
      return "chưa có";
    }
    var date = new Date(dateValue);
    if (Number.isNaN(date.getTime())) {
      return "chưa có";
    }
    var dd = String(date.getDate()).padStart(2, "0");
    var mm = String(date.getMonth() + 1).padStart(2, "0");
    var yyyy = date.getFullYear();
    return dd + "/" + mm + "/" + yyyy;
  }

  function applySidebarProfile(profileInput) {
    var profile = profileInput || TamTai.getProfile();
    var heading = document.querySelector(".profile-head h2");
    var emailText = document.querySelector(".profile-head p");
    if (heading) {
      heading.textContent = displayValue(profile.fullName);
    }
    if (emailText) {
      emailText.textContent = displayValue(profile.email);
    }
  }

  function renderEmpty(message) {
    var list = document.getElementById("reviewList");
    if (!list) {
      return;
    }
    list.innerHTML = '<p class="review-empty">' + escapeHtml(message || "chưa có dữ liệu") + "</p>";
  }

  async function ensureCustomerContext() {
    var token = localStorage.getItem("access_token");
    var role = TamTai.getRole();
    if (!token || role !== "user") {
      return false;
    }

    state.token = token;

    try {
      var response = await fetch(TamTai.API_BASE_URL + "/customers/me", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token
        }
      });

      if (!response.ok) {
        return false;
      }

      var customer = await response.json();
      state.customerId = customer.customer_id || "";

      var mapped = {
        fullName: customer.customer_name || "",
        email: customer.customer_email || "",
        phone: customer.phone_number || "",
        address: customer.address || ""
      };

      localStorage.setItem("tamtai_customer_id", state.customerId);
      localStorage.setItem("tamtai_customer_profile", JSON.stringify(customer));
      TamTai.saveProfile(mapped);
      applySidebarProfile(mapped);

      return Boolean(state.customerId);
    } catch (error) {
      return false;
    }
  }

  async function fetchProducts() {
    try {
      var response = await fetch(TamTai.API_BASE_URL + "/products?skip=0&limit=100", {
        method: "GET"
      });
      if (!response.ok) {
        return [];
      }
      var data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (error) {
      return [];
    }
  }

  async function fetchMyReviews() {
    if (!state.customerId || !state.token) {
      return {};
    }

    try {
      var response = await fetch(
        TamTai.API_BASE_URL + "/reviews/customer/" + encodeURIComponent(state.customerId),
        {
          method: "GET",
          headers: {
            Authorization: "Bearer " + state.token
          }
        }
      );

      if (!response.ok) {
        return {};
      }

      var rows = await response.json();
      if (!Array.isArray(rows)) {
        return {};
      }

      var map = {};
      rows.forEach(function (review) {
        var productId = String(review.product_id || "").trim();
        if (!productId) {
          return;
        }
        var existing = map[productId];
        if (!existing) {
          map[productId] = review;
          return;
        }

        var currentTime = new Date(review.created_at || 0).getTime();
        var existingTime = new Date(existing.created_at || 0).getTime();
        if (currentTime >= existingTime) {
          map[productId] = review;
        }
      });

      return map;
    } catch (error) {
      return {};
    }
  }

  function buildReviewProductList(products, reviewsByProduct) {
    var byId = {};
    products.forEach(function (product) {
      byId[product.product_id] = product;
    });

    var result = [];
    Object.keys(reviewsByProduct).forEach(function (productId) {
      if (byId[productId]) {
        result.push(byId[productId]);
      } else {
        result.push({
          product_id: productId,
          product_name: "Sản phẩm " + productId,
          description: null,
          image_url: null
        });
      }
    });

    products.forEach(function (product) {
      if (result.length >= 10) {
        return;
      }
      if (!reviewsByProduct[product.product_id]) {
        result.push(product);
      }
    });

    return result.slice(0, 10);
  }

  function createStarsHtml(selectedRating) {
    var html = "";
    for (var i = 1; i <= 5; i += 1) {
      var activeClass = i <= selectedRating ? " active" : "";
      html += '<button type="button" class="star-btn' + activeClass + '" data-value="' + i + '">&#9733;</button>';
    }
    return html;
  }

  function createReviewCard(product) {
    var review = state.reviewsByProduct[product.product_id] || null;
    var rating = review ? Number(review.rating || 0) : 0;
    var ratingText = rating > 0 ? ("Bạn đã chọn " + rating + " sao") : "Chưa chọn sao";
    var buttonText = review ? "Cập nhật đánh giá" : "Gửi đánh giá";
    var reviewedAt = review ? formatDate(review.created_at) : "chưa có";
    var image = product.image_url || DEFAULT_IMAGE;

    return [
      '<article class="review-item" data-product-id="' + escapeHtml(product.product_id) + '">',
      '  <div class="review-product">',
      '    <img src="' + escapeHtml(image) + '" alt="Sản phẩm">',
      "    <div>",
      "      <h3>" + escapeHtml(displayValue(product.product_name)) + "</h3>",
      "      <p>Mã sản phẩm: " + escapeHtml(displayValue(product.product_id)) + " | Đã đánh giá: " + escapeHtml(reviewedAt) + "</p>",
      '      <p class="review-meta">' + escapeHtml(displayValue(product.description)) + "</p>",
      "    </div>",
      "  </div>",
      '  <div class="review-actions-top">',
      '    <a class="buy-again-btn" href="../cart/cart.html">Mua lại</a>',
      "  </div>",
      '  <form class="review-form">',
      "    <label>Đánh giá sao</label>",
      '    <div class="star-picker">',
      createStarsHtml(rating),
      '      <span class="rating-text">' + escapeHtml(ratingText) + "</span>",
      "    </div>",
      '    <input class="rating-value" type="hidden" value="' + String(rating || 0) + '">',
      "    <label>Nhận xét của bạn</label>",
      '    <textarea class="review-comment" rows="4" placeholder="Chia sẻ trải nghiệm sử dụng sản phẩm...">' + escapeHtml(review ? (review.comment || "") : "") + "</textarea>",
      "    <label>Hình ảnh sản phẩm</label>",
      '    <input class="review-images" type="file" accept="image/*" multiple>',
      '    <p class="image-count">Chưa chọn hình ảnh</p>',
      '    <button type="submit" class="submit-review-btn">' + buttonText + "</button>",
      "  </form>",
      "</article>"
    ].join("");
  }

  function renderReviewList(products) {
    var list = document.getElementById("reviewList");
    if (!list) {
      return;
    }

    if (!products.length) {
      renderEmpty("chưa có sản phẩm để đánh giá");
      return;
    }

    list.innerHTML = products.map(createReviewCard).join("");
    bindReviewItems();
  }

  function updateStarsVisual(item, rating) {
    var stars = item.querySelectorAll(".star-btn");
    var ratingText = item.querySelector(".rating-text");
    stars.forEach(function (star) {
      var starValue = Number(star.getAttribute("data-value"));
      star.classList.toggle("active", starValue <= rating);
    });
    if (ratingText) {
      ratingText.textContent = rating > 0 ? ("Bạn đã chọn " + rating + " sao") : "Chưa chọn sao";
    }
  }

  async function submitReview(productId, rating, comment) {
    var response = await fetch(TamTai.API_BASE_URL + "/reviews/", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + state.token,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        product_id: productId,
        customer_id: state.customerId,
        rating: rating,
        comment: comment || null
      })
    });

    var data = await response.json();
    if (!response.ok) {
      throw new Error((data && data.detail) || "Không gửi được đánh giá.");
    }
    return data;
  }

  function bindReviewItems() {
    var reviewItems = document.querySelectorAll(".review-item");

    reviewItems.forEach(function (item) {
      var stars = item.querySelectorAll(".star-btn");
      var ratingValue = item.querySelector(".rating-value");
      var fileInput = item.querySelector(".review-images");
      var imageCount = item.querySelector(".image-count");
      var form = item.querySelector(".review-form");

      stars.forEach(function (star) {
        star.addEventListener("click", function () {
          var value = Number(star.getAttribute("data-value") || 0);
          if (ratingValue) {
            ratingValue.value = String(value);
          }
          updateStarsVisual(item, value);
        });
      });

      if (fileInput && imageCount) {
        fileInput.addEventListener("change", function () {
          var count = fileInput.files ? fileInput.files.length : 0;
          imageCount.textContent = count > 0 ? ("Đã chọn " + count + " hình ảnh") : "Chưa chọn hình ảnh";
        });
      }

      if (!form) {
        return;
      }

      form.addEventListener("submit", async function (event) {
        event.preventDefault();

        var productId = item.getAttribute("data-product-id");
        var rating = Number((ratingValue && ratingValue.value) || 0);
        var commentInput = form.querySelector(".review-comment");
        var comment = commentInput ? commentInput.value.trim() : "";
        var submitBtn = form.querySelector(".submit-review-btn");

        if (!productId) {
          alert("Không tìm thấy mã sản phẩm.");
          return;
        }

        if (rating < 1 || rating > 5) {
          alert("Vui lòng chọn số sao trước khi gửi đánh giá.");
          return;
        }

        if (!comment) {
          alert("Vui lòng nhập nhận xét của bạn.");
          return;
        }

        if (submitBtn) {
          submitBtn.disabled = true;
        }

        try {
          var saved = await submitReview(productId, rating, comment);
          state.reviewsByProduct[productId] = saved;
          updateStarsVisual(item, rating);
          if (submitBtn) {
            submitBtn.textContent = "Cập nhật đánh giá";
          }
          alert("Đã lưu đánh giá vào hệ thống.");
        } catch (error) {
          alert(error.message || "Không gửi được đánh giá.");
        } finally {
          if (submitBtn) {
            submitBtn.disabled = false;
          }
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", async function () {
    TamTai.setupSearchRedirect(".search-box input", "../products/products.html");
    TamTai.showAdminMenuLink(document);
    applySidebarProfile();

    var canUse = await ensureCustomerContext();
    if (!canUse) {
      renderEmpty("bạn cần đăng nhập để xem và gửi đánh giá");
      return;
    }

    var products = await fetchProducts();
    var reviewsMap = await fetchMyReviews();

    state.products = products;
    state.reviewsByProduct = reviewsMap;

    var reviewProducts = buildReviewProductList(products, reviewsMap);
    renderReviewList(reviewProducts);
  });
})();
