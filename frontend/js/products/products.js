(function () {
  var DEFAULT_IMAGE = (window.TamTai && TamTai.DEFAULT_PRODUCT_IMAGE) || "../../images/acer-refurbished-laptop-500x500.webp";
  var BASE_VISIBLE_ITEMS = 9;

  var CATEGORY_PRIORITY = [
    "CAT_PHONE",
    "CAT_LAPTOP",
    "CAT_HEADPHONE",
    "CAT_SMARTWATCH",
    "CAT_KEYBOARD",
    "CAT_MOUSE"
  ];

  var CATEGORY_LABELS = {
    CAT_PHONE: "\u0110i\u1ec7n tho\u1ea1i",
    CAT_LAPTOP: "Laptop",
    CAT_HEADPHONE: "Tai nghe",
    CAT_SMARTWATCH: "\u0110\u1ed3ng h\u1ed3 th\u00f4ng minh",
    CAT_KEYBOARD: "B\u00e0n ph\u00edm",
    CAT_MOUSE: "Chu\u1ed9t m\u00e1y t\u00ednh"
  };

  var PRICE_RANGES = [
    { key: "lt100", label: "< 100k", test: function (price) { return price < 100000; } },
    { key: "100_500", label: "100k - 500k", test: function (price) { return price >= 100000 && price <= 500000; } },
    { key: "500_2000", label: "500k - 2 tri\u1ec7u", test: function (price) { return price > 500000 && price <= 2000000; } },
    { key: "2000_10000", label: "2 tri\u1ec7u - 10 tri\u1ec7u", test: function (price) { return price > 2000000 && price <= 10000000; } },
    { key: "gt10000", label: "> 10 tri\u1ec7u", test: function (price) { return price > 10000000; } }
  ];

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

  function toNumber(value, fallback) {
    var number = Number(value);
    return Number.isFinite(number) ? number : fallback;
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

  function categoryLabel(categoryId, fallbackName) {
    if (CATEGORY_LABELS[categoryId]) {
      return CATEGORY_LABELS[categoryId];
    }

    var normalized = normalizeText(fallbackName || "");
    if (normalized === "dien thoai") {
      return "\u0110i\u1ec7n tho\u1ea1i";
    }
    if (normalized === "dong ho thong minh") {
      return "\u0110\u1ed3ng h\u1ed3 th\u00f4ng minh";
    }
    if (normalized === "ban phim") {
      return "B\u00e0n ph\u00edm";
    }
    if (normalized === "chuot may tinh") {
      return "Chu\u1ed9t m\u00e1y t\u00ednh";
    }
    return fallbackName || categoryId || "Kh\u00e1c";
  }

  function getCategoryPriority(categoryId) {
    var idx = CATEGORY_PRIORITY.indexOf(categoryId);
    return idx === -1 ? 999 : idx;
  }

  function compareCategories(a, b) {
    var pa = getCategoryPriority(a.category_id);
    var pb = getCategoryPriority(b.category_id);
    if (pa !== pb) {
      return pa - pb;
    }
    return categoryLabel(a.category_id, a.category_name).localeCompare(categoryLabel(b.category_id, b.category_name), "vi");
  }

  function getPriceBeforeDiscount(price, discountPercent) {
    if (!discountPercent || discountPercent <= 0 || discountPercent >= 100) {
      return price;
    }

    var before = (price * 100) / (100 - discountPercent);
    return Math.round(before);
  }

  function resolveCategoryIdFromQuery(rawCategory, categoriesById) {
    if (!rawCategory) {
      return "";
    }

    var input = String(rawCategory).trim();
    if (!input) {
      return "";
    }

    if (categoriesById[input]) {
      return input;
    }

    var normalized = normalizeText(input);
    var aliases = {
      "dien thoai": "CAT_PHONE",
      "laptop": "CAT_LAPTOP",
      "tai nghe": "CAT_HEADPHONE",
      "dong ho": "CAT_SMARTWATCH",
      "dong ho thong minh": "CAT_SMARTWATCH",
      "ban phim": "CAT_KEYBOARD",
      "chuot": "CAT_MOUSE",
      "chuot may tinh": "CAT_MOUSE",
      "phone": "CAT_PHONE",
      "headphone": "CAT_HEADPHONE",
      "watch": "CAT_SMARTWATCH",
      "keyboard": "CAT_KEYBOARD",
      "mouse": "CAT_MOUSE"
    };

    if (aliases[normalized] && categoriesById[aliases[normalized]]) {
      return aliases[normalized];
    }

    var matched = Object.values(categoriesById).find(function (category) {
      var categoryName = normalizeText(categoryLabel(category.category_id, category.category_name));
      return categoryName === normalized || categoryName.indexOf(normalized) !== -1 || normalized.indexOf(categoryName) !== -1;
    });

    return matched ? matched.category_id : "";
  }

  function sortProducts(list, sortMode) {
    var cloned = list.slice();

    if (sortMode === 1) {
      cloned.sort(function (a, b) { return a.price - b.price; });
    } else if (sortMode === 2) {
      cloned.sort(function (a, b) { return b.price - a.price; });
    } else if (sortMode === 3) {
      cloned.sort(function (a, b) {
        if (b.totalReviews !== a.totalReviews) {
          return b.totalReviews - a.totalReviews;
        }
        if (b.ratingAvg !== a.ratingAvg) {
          return b.ratingAvg - a.ratingAvg;
        }
        return a.orderIndex - b.orderIndex;
      });
    } else {
      cloned.sort(function (a, b) { return a.orderIndex - b.orderIndex; });
    }

    return cloned;
  }

  function matchPriceRange(price, selectedRanges) {
    if (!selectedRanges.size) {
      return true;
    }

    return PRICE_RANGES.some(function (range) {
      return selectedRanges.has(range.key) && range.test(price);
    });
  }

  function buildProductCard(product) {
    var oldPrice = getPriceBeforeDiscount(product.price, product.discountPercent);
    var hasDiscount = oldPrice > product.price;

    return [
      '<article class="product-card" data-product-id="' + escapeHtml(product.id) + '">',
      '  <div class="product-image"><img src="' + escapeHtml(product.image) + '" alt="' + escapeHtml(product.name) + '"></div>',
      '  <h3>' + escapeHtml(product.name) + '</h3>',
      '  <div class="price-row">',
      '    <p class="current-price">' + TamTai.formatCurrency(product.price) + '</p>',
      hasDiscount ? ('    <span class="old-price">' + TamTai.formatCurrency(oldPrice) + '</span>') : '',
      hasDiscount ? ('    <span class="discount-badge">-' + escapeHtml(product.discountPercent) + '%</span>') : '',
      '  </div>',
      '  <div class="product-extra">',
      '    <span class="rating"><i class="fa-solid fa-star"></i> ' + escapeHtml(product.ratingAvg.toFixed(1)) + ' (' + escapeHtml(product.totalReviews) + ')</span>',
      '    <span>T\u1ed3n: ' + escapeHtml(product.stockQuantity) + '</span>',
      '  </div>',
      '  <div class="product-actions">',
      '    <button type="button" class="btn-add-cart" data-action="add-cart">Th\u00eam v\u00e0o gi\u1ecf</button>',
      '    <button type="button" class="btn-buy-now" data-action="buy-now">Mua ngay</button>',
      '  </div>',
      '</article>'
    ].join('');
  }

  function toCartItem(product) {
    return {
      id: product.id,
      productId: product.id,
      categoryId: product.categoryId,
      name: product.name,
      price: product.price,
      oldPrice: getPriceBeforeDiscount(product.price, product.discountPercent),
      image: product.image
    };
  }

  function isLoggedIn() {
    var token = localStorage.getItem('access_token');
    var hasToken = Boolean(token && String(token).trim());
    if (!hasToken) {
      return false;
    }

    if (window.TamTai && typeof TamTai.getRole === 'function') {
      return TamTai.getRole() !== 'guest';
    }

    var role = localStorage.getItem('tamtai_role') || 'guest';
    return role !== 'guest';
  }

  function toggleGuestOnlyElements() {
    var loggedIn = isLoggedIn();
    var guestOnlyElements = document.querySelectorAll('[data-guest-only]');

    guestOnlyElements.forEach(function (element) {
      element.style.display = loggedIn ? 'none' : '';
    });
  }

  async function loadCatalog() {
    var categoriesData = await TamTai.fetchJson('/categories?skip=0&limit=100');
    var productsData = await TamTai.fetchJson('/products?skip=0&limit=100');

    var categories = Array.isArray(categoriesData) ? categoriesData : [];
    var products = Array.isArray(productsData) ? productsData : [];

    var categoriesById = {};
    categories.forEach(function (category) {
      categoriesById[category.category_id] = category;
    });

    var normalizedProducts = products.map(function (product, index) {
      var category = categoriesById[product.category_id] || null;

      return {
        id: String(product.product_id),
        categoryId: String(product.category_id || ''),
        categoryName: categoryLabel(product.category_id, category && category.category_name),
        name: String(product.product_name || 'S\u1ea3n ph\u1ea9m'),
        description: String(product.description || ''),
        image: toImageSrc(product.image_url),
        price: toNumber(product.unit_price, 0),
        discountPercent: toNumber(product.discount_percent, 0),
        stockQuantity: toNumber(product.stock_quantity, 0),
        ratingAvg: toNumber(product.rating_avg, 0),
        totalReviews: toNumber(product.total_reviews, 0),
        orderIndex: index
      };
    });

    return {
      categories: categories,
      categoriesById: categoriesById,
      products: normalizedProducts
    };
  }

  function renderCategoryFilters(filterBlock, categories, categoryCounts) {
    if (!filterBlock) {
      return;
    }

    var total = categories.reduce(function (sum, category) {
      return sum + (categoryCounts[category.category_id] || 0);
    }, 0);

    var html = [];
    html.push('<h2>Danh m\u1ee5c</h2>');
    html.push('<label><input type="checkbox" data-filter-type="category" data-category="all"> T\u1ea5t c\u1ea3 (' + total + ')</label>');

    categories.forEach(function (category) {
      var count = categoryCounts[category.category_id] || 0;
      html.push(
        '<label><input type="checkbox" data-filter-type="category" data-category="' + escapeHtml(category.category_id) + '"> '
        + escapeHtml(categoryLabel(category.category_id, category.category_name))
        + ' (' + count + ')</label>'
      );
    });

    filterBlock.innerHTML = html.join('');
  }

  function renderPriceFilters(filterBlock) {
    if (!filterBlock) {
      return;
    }

    var html = [];
    html.push('<h2>Kho\u1ea3ng gi\u00e1</h2>');
    PRICE_RANGES.forEach(function (range) {
      html.push(
        '<label><input type="checkbox" data-filter-type="price" data-price-range="' + escapeHtml(range.key) + '"> '
        + escapeHtml(range.label)
        + '</label>'
      );
    });

    filterBlock.innerHTML = html.join('');
  }

  function syncCategoryInputs(filterBlock, selectedCategories) {
    if (!filterBlock) {
      return;
    }

    filterBlock.querySelectorAll('input[data-filter-type="category"]').forEach(function (input) {
      var value = input.getAttribute('data-category');
      if (value === 'all') {
        input.checked = selectedCategories.size === 0;
      } else {
        input.checked = selectedCategories.has(value);
      }
    });
  }

  function syncPriceInputs(filterBlock, selectedRanges) {
    if (!filterBlock) {
      return;
    }

    filterBlock.querySelectorAll('input[data-filter-type="price"]').forEach(function (input) {
      var value = input.getAttribute('data-price-range');
      input.checked = selectedRanges.has(value);
    });
  }

  function attachQuickCategoryIds(quickItems, categoriesById) {
    quickItems.forEach(function (item) {
      var label = normalizeText(item.textContent);
      var categoryId = resolveCategoryIdFromQuery(label, categoriesById);
      if (categoryId) {
        item.setAttribute('data-category-id', categoryId);
      }
    });
  }

  function syncQuickItems(quickItems, selectedCategories) {
    quickItems.forEach(function (item) {
      var itemCategoryId = item.getAttribute('data-category-id') || '';
      var active = selectedCategories.size === 1 && selectedCategories.has(itemCategoryId);
      item.classList.toggle('active', active);
    });
  }

  document.addEventListener('DOMContentLoaded', async function () {
    TamTai.setupSearchRedirect('.search-box input', '../products/products.html');
    toggleGuestOnlyElements();

    window.addEventListener('storage', function (event) {
      if (event.key === 'access_token' || event.key === 'tamtai_role') {
        toggleGuestOnlyElements();
      }
    });

    var grid = document.querySelector('.product-grid');
    var moreBtn = document.querySelector('.more-btn');
    var sortSelect = document.querySelector('.filter-block select');
    var quickItems = Array.prototype.slice.call(document.querySelectorAll('.quick-item'));
    var searchInput = document.querySelector('.search-box input');
    var heading = document.querySelector('.products-head h2');
    var filterBlocks = document.querySelectorAll('.filter-panel .filter-block');
    var categoryFilterBlock = filterBlocks[0] || null;
    var priceFilterBlock = filterBlocks[1] || null;

    if (!grid) {
      return;
    }

    grid.innerHTML = '<p class="empty-products">\u0110ang t\u1ea3i d\u1eef li\u1ec7u s\u1ea3n ph\u1ea9m...</p>';

    try {
      var catalog = await loadCatalog();
      var products = catalog.products;
      var productById = {};
      products.forEach(function (product) {
        productById[product.id] = product;
      });

      var categoryCounts = {};
      products.forEach(function (product) {
        categoryCounts[product.categoryId] = (categoryCounts[product.categoryId] || 0) + 1;
      });

      var categories = catalog.categories
        .filter(function (category) { return categoryCounts[category.category_id] > 0; })
        .sort(compareCategories);

      renderCategoryFilters(categoryFilterBlock, categories, categoryCounts);
      renderPriceFilters(priceFilterBlock);
      attachQuickCategoryIds(quickItems, catalog.categoriesById);

      var params = new URLSearchParams(window.location.search);
      var initialKeywordRaw = params.get('q') || '';
      var initialKeyword = normalizeText(initialKeywordRaw);
      var initialCategoryId = resolveCategoryIdFromQuery(params.get('category'), catalog.categoriesById);

      var state = {
        selectedCategories: new Set(initialCategoryId ? [initialCategoryId] : []),
        selectedPriceRanges: new Set(),
        keyword: initialKeyword,
        sortMode: sortSelect ? sortSelect.selectedIndex : 0,
        expanded: false,
        render: function () {
          syncCategoryInputs(categoryFilterBlock, state.selectedCategories);
          syncPriceInputs(priceFilterBlock, state.selectedPriceRanges);
          syncQuickItems(quickItems, state.selectedCategories);

          var filtered = products.filter(function (product) {
            var byCategory = state.selectedCategories.size === 0 || state.selectedCategories.has(product.categoryId);
            var byPrice = matchPriceRange(product.price, state.selectedPriceRanges);
            var byKeyword = true;

            if (state.keyword) {
              var haystack = normalizeText(product.name + ' ' + product.description + ' ' + product.categoryName);
              byKeyword = haystack.indexOf(state.keyword) !== -1;
            }

            return byCategory && byPrice && byKeyword;
          });

          var sorted = sortProducts(filtered, state.sortMode);
          var visibleCount = state.expanded ? sorted.length : BASE_VISIBLE_ITEMS;
          var visible = sorted.slice(0, visibleCount);

          if (!visible.length) {
            grid.innerHTML = '<p class="empty-products">Kh\u00f4ng t\u00ecm th\u1ea5y s\u1ea3n ph\u1ea9m ph\u00f9 h\u1ee3p.</p>';
          } else {
            grid.innerHTML = visible.map(buildProductCard).join('');
          }

          if (heading) {
            heading.textContent = 'S\u1ea2N PH\u1ea8M (' + filtered.length + ')';
          }

          if (moreBtn) {
            if (sorted.length <= BASE_VISIBLE_ITEMS) {
              moreBtn.style.display = 'none';
            } else {
              moreBtn.style.display = 'inline-flex';
              moreBtn.textContent = state.expanded ? 'Thu g\u1ecdn danh s\u00e1ch' : 'Xem t\u1ea5t c\u1ea3 s\u1ea3n ph\u1ea9m';
            }
          }
        }
      };

      if (searchInput && initialKeywordRaw) {
        searchInput.value = initialKeywordRaw;
      }

      if (categoryFilterBlock) {
        categoryFilterBlock.addEventListener('change', function (event) {
          var input = event.target.closest('input[data-filter-type="category"]');
          if (!input) {
            return;
          }

          var value = input.getAttribute('data-category');
          if (value === 'all') {
            state.selectedCategories.clear();
          } else {
            if (input.checked) {
              state.selectedCategories.add(value);
            } else {
              state.selectedCategories.delete(value);
            }
          }

          state.expanded = false;
          state.render();
        });
      }

      if (priceFilterBlock) {
        priceFilterBlock.addEventListener('change', function (event) {
          var input = event.target.closest('input[data-filter-type="price"]');
          if (!input) {
            return;
          }

          var key = input.getAttribute('data-price-range');
          if (input.checked) {
            state.selectedPriceRanges.add(key);
          } else {
            state.selectedPriceRanges.delete(key);
          }

          state.expanded = false;
          state.render();
        });
      }

      quickItems.forEach(function (item) {
        item.addEventListener('click', function (event) {
          event.preventDefault();
          var categoryId = item.getAttribute('data-category-id') || '';

          state.selectedCategories.clear();
          if (categoryId) {
            state.selectedCategories.add(categoryId);
          }

          state.expanded = false;
          state.render();
        });
      });

      if (searchInput) {
        searchInput.addEventListener('input', function () {
          state.keyword = normalizeText(searchInput.value);
          state.expanded = false;
          state.render();
        });
      }

      if (sortSelect) {
        sortSelect.addEventListener('change', function () {
          state.sortMode = sortSelect.selectedIndex;
          state.render();
        });
      }

      if (moreBtn) {
        moreBtn.addEventListener('click', function (event) {
          event.preventDefault();
          state.expanded = !state.expanded;
          state.render();
        });
      }

      grid.addEventListener('click', function (event) {
        var actionButton = event.target.closest('button[data-action]');
        if (actionButton) {
          event.preventDefault();
          event.stopPropagation();

          var cardForAction = actionButton.closest('.product-card[data-product-id]');
          if (!cardForAction) {
            return;
          }

          var productId = cardForAction.getAttribute('data-product-id');
          var action = actionButton.getAttribute('data-action');
          var product = productById[productId];
          if (!product) {
            return;
          }

          if (action === 'add-cart') {
            TamTai.addToCart(toCartItem(product), 1);
            window.location.href = '../cart/cart.html';
            return;
          }

          if (action === 'buy-now') {
            TamTai.addToCart(toCartItem(product), 1);
            window.location.href = '../cart/checkout.html?from=buy-now';
            return;
          }
        }

        var card = event.target.closest('.product-card[data-product-id]');
        if (!card) {
          return;
        }

        var productIdForDetail = card.getAttribute('data-product-id');
        if (!productIdForDetail) {
          return;
        }

        window.location.href = '../products/product-detail.html?id=' + encodeURIComponent(productIdForDetail);
      });

      state.render();
    } catch (error) {
      grid.innerHTML = '<p class="empty-products">Kh\u00f4ng th\u1ec3 t\u1ea3i d\u1eef li\u1ec7u s\u1ea3n ph\u1ea9m. Vui l\u00f2ng th\u1eed l\u1ea1i.</p>';
      if (moreBtn) {
        moreBtn.style.display = 'none';
      }
      if (heading) {
        heading.textContent = 'S\u1ea2N PH\u1ea8M';
      }
    }
  });
})();



