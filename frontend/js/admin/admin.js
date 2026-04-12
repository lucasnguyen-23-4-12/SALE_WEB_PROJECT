(function () {
  var state = {
    currentView: 'dashboard',
    categories: [],
    products: [],
    orders: [],
    customers: [],
    discountCodes: [],
    dashboard: null,
    editingProductId: '',
    editingCustomerId: '',
    editingDiscountId: ''
  };

  var ORDER_STATUSES = ['Pending', 'Confirmed', 'Shipping', 'Delivered', 'Cancelled'];

  function redirectToLogin() {
    window.location.href = '../auth/login.html?redirect=admin';
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function formatMoney(value) {
    return TamTai.formatCurrency(Number(value || 0));
  }

  function formatDate(value) {
    if (!value) {
      return '-';
    }

    var date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return String(value);
    }

    return date.toLocaleDateString('vi-VN');
  }

  function formatDateTimeLocal(value) {
    if (!value) {
      return '';
    }

    var date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return '';
    }

    var pad = function (part) {
      return String(part).padStart(2, '0');
    };

    return [
      date.getFullYear(),
      '-',
      pad(date.getMonth() + 1),
      '-',
      pad(date.getDate()),
      'T',
      pad(date.getHours()),
      ':',
      pad(date.getMinutes())
    ].join('');
  }

  function toImageSrc(imageUrl) {
    var raw = String(imageUrl || '').trim();
    if (!raw) {
      return TamTai.DEFAULT_PRODUCT_IMAGE;
    }

    if (/^https?:\/\//i.test(raw) || raw.indexOf('data:') === 0) {
      return raw;
    }

    return TamTai.buildApiUrl(raw.indexOf('/') === 0 ? raw : '/' + raw);
  }

  function normalizeSearchValue(value) {
    return String(value || '').trim();
  }

  function showMessage(message, type) {
    var box = document.getElementById('pageMessage');
    if (!box) {
      return;
    }

    if (!message) {
      box.textContent = '';
      box.className = 'page-message';
      return;
    }

    box.textContent = message;
    box.className = 'page-message visible ' + (type || 'info');
  }

  function getAuthHeaders(extraHeaders) {
    var token = localStorage.getItem('access_token');
    return Object.assign({ Authorization: 'Bearer ' + token }, extraHeaders || {});
  }

  async function request(path, options) {
    var response = await fetch(TamTai.API_BASE_URL + path, Object.assign({}, options || {}, {
      headers: getAuthHeaders((options && options.headers) || {})
    }));

    if (response.status === 401 || response.status === 403) {
      TamTai.clearSession();
      redirectToLogin();
      throw new Error('Phiên đăng nhập admin đã hết hạn.');
    }

    var raw = await response.text();
    var data = null;
    if (raw) {
      try {
        data = JSON.parse(raw);
      } catch (error) {
        data = raw;
      }
    }

    if (!response.ok) {
      throw new Error((data && data.detail) || (data && data.error && data.error.message) || 'Yêu cầu thất bại.');
    }

    return data;
  }

  async function verifyAdminAccess() {
    if (TamTai.getRole() !== 'admin' || !localStorage.getItem('access_token')) {
      redirectToLogin();
      return false;
    }

    try {
      await request('/admin/me');
      return true;
    } catch (error) {
      showMessage(error.message || 'Không thể xác minh quyền admin.', 'error');
      return false;
    }
  }

  function getStatusMeta(status) {
    var normalized = String(status || '').trim().toLowerCase();
    if (normalized.indexOf('deliver') !== -1 || normalized.indexOf('done') !== -1) {
      return { label: 'Đã giao', className: 'status-success' };
    }
    if (normalized.indexOf('ship') !== -1) {
      return { label: 'Đang giao', className: 'status-warning' };
    }
    if (normalized.indexOf('cancel') !== -1) {
      return { label: 'Đã hủy', className: 'status-danger' };
    }
    if (normalized.indexOf('confirm') !== -1) {
      return { label: 'Đã xác nhận', className: 'status-warning' };
    }
    if (normalized.indexOf('pend') !== -1) {
      return { label: 'Chờ xử lý', className: 'status-neutral' };
    }
    return { label: status || 'Không rõ', className: 'status-neutral' };
  }

  function setActiveView(viewName) {
    state.currentView = viewName;
    document.querySelectorAll('.menu-link').forEach(function (button) {
      button.classList.toggle('active', button.getAttribute('data-view-target') === viewName);
    });
    document.querySelectorAll('.view-section').forEach(function (section) {
      section.classList.toggle('active', section.getAttribute('data-view') === viewName);
    });
  }

  function syncGlobalSearchFromView() {
    var globalSearch = document.getElementById('adminGlobalSearch');
    if (!globalSearch) {
      return;
    }

    var sourceMap = {
      products: 'productSearch',
      orders: 'orderSearch',
      customers: 'customerSearch',
      discounts: 'discountSearch'
    };
    var source = sourceMap[state.currentView] ? document.getElementById(sourceMap[state.currentView]) : null;
    globalSearch.value = source ? source.value : '';
  }

  function renderStats() {
    var stats = state.dashboard && state.dashboard.stats ? state.dashboard.stats : null;
    if (!stats) {
      return;
    }

    document.getElementById('statProducts').textContent = stats.total_products || 0;
    document.getElementById('statCustomers').textContent = stats.total_customers || 0;
    document.getElementById('statOrders').textContent = stats.total_orders || 0;
    document.getElementById('statRevenue').textContent = formatMoney(stats.total_revenue || 0);
    document.getElementById('statCategories').textContent = stats.total_categories || 0;
    document.getElementById('statPendingOrders').textContent = stats.pending_orders || 0;
    document.getElementById('statLowStock').textContent = stats.low_stock_products || 0;
    document.getElementById('statDiscountCodes').textContent = stats.active_discount_codes || 0;
  }

  function renderEmptyRow(colspan, message) {
    return '<tr><td colspan="' + colspan + '"><div class="empty-state">' + escapeHtml(message) + '</div></td></tr>';
  }

  function renderDashboard() {
    renderStats();

    var ordersTable = document.getElementById('dashboardOrdersTable');
    var recentOrders = state.dashboard && Array.isArray(state.dashboard.recent_orders) ? state.dashboard.recent_orders : [];
    if (ordersTable) {
      ordersTable.innerHTML = recentOrders.length ? recentOrders.map(function (order) {
        var status = getStatusMeta(order.status);
        return [
          '<tr>',
          '  <td>' + escapeHtml(order.order_id) + '</td>',
          '  <td>' + escapeHtml(order.customer_name || order.customer_email || '-') + '</td>',
          '  <td><span class="status-chip ' + status.className + '">' + escapeHtml(status.label) + '</span></td>',
          '  <td class="money-text">' + escapeHtml(formatMoney(order.total_amount || 0)) + '</td>',
          '  <td>' + escapeHtml(formatDate(order.order_date)) + '</td>',
          '</tr>'
        ].join('');
      }).join('') : renderEmptyRow(5, 'Chưa có đơn hàng nào.');
    }

    function renderMiniList(targetId, items, emptyText) {
      var node = document.getElementById(targetId);
      if (!node) {
        return;
      }
      if (!items.length) {
        node.innerHTML = '<div class="empty-state">' + escapeHtml(emptyText) + '</div>';
        return;
      }

      node.innerHTML = items.map(function (item) {
        var secondary = item.category_name ? ('Danh mục: ' + item.category_name + ' | ') : '';
        secondary += 'Tồn: ' + (item.stock_quantity || 0) + ' | Đã bán: ' + (item.sold_quantity || 0);
        return [
          '<article class="mini-item">',
          '  <div>',
          '    <strong>' + escapeHtml(item.product_name || '-') + '</strong>',
          '    <span>' + escapeHtml(secondary) + '</span>',
          '  </div>',
          '  <div class="money-text">' + escapeHtml(formatMoney(item.unit_price || 0)) + '</div>',
          '</article>'
        ].join('');
      }).join('');
    }

    renderMiniList('dashboardTopProducts', (state.dashboard && state.dashboard.top_products) || [], 'Chưa có sản phẩm nổi bật.');
    renderMiniList('dashboardLowStock', (state.dashboard && state.dashboard.low_stock_products) || [], 'Không có sản phẩm sắp hết hàng.');
  }

  function populateCategoryOptions() {
    var filter = document.getElementById('productCategoryFilter');
    var formSelect = document.getElementById('productCategory');
    var options = state.categories.map(function (category) {
      return '<option value="' + escapeHtml(category.category_id) + '">' + escapeHtml(category.category_name) + '</option>';
    }).join('');

    if (filter) {
      var current = filter.value;
      filter.innerHTML = '<option value="">Tất cả danh mục</option>' + options;
      filter.value = current || '';
    }

    if (formSelect) {
      var selected = formSelect.value;
      formSelect.innerHTML = '<option value="">Chọn danh mục</option>' + options;
      formSelect.value = selected || '';
    }
  }

  function populateDiscountTargets() {
    var productSelect = document.getElementById('discountProduct');
    var customerSelect = document.getElementById('discountCustomer');
    if (productSelect) {
      var productValue = productSelect.value;
      productSelect.innerHTML = '<option value="">Tất cả sản phẩm</option>' + state.products.map(function (product) {
        return '<option value="' + escapeHtml(product.product_id) + '">' + escapeHtml(product.product_name) + '</option>';
      }).join('');
      productSelect.value = productValue || '';
    }

    if (customerSelect) {
      var customerValue = customerSelect.value;
      customerSelect.innerHTML = '<option value="">Tất cả người dùng</option>' + state.customers.map(function (customer) {
        return '<option value="' + escapeHtml(customer.customer_id) + '">' + escapeHtml(customer.customer_name + ' - ' + customer.customer_email) + '</option>';
      }).join('');
      customerSelect.value = customerValue || '';
    }
  }

  function renderProducts() {
    document.getElementById('productsMeta').textContent = state.products.length + ' sản phẩm';
    populateDiscountTargets();

    var body = document.getElementById('productsTableBody');
    if (!body) {
      return;
    }

    body.innerHTML = state.products.length ? state.products.map(function (product) {
      return [
        '<tr>',
        '  <td>' + escapeHtml(product.product_id) + '</td>',
        '  <td>',
        '    <div class="product-cell">',
        '      <div class="product-thumb"><img src="' + escapeHtml(toImageSrc(product.image_url)) + '" alt="' + escapeHtml(product.product_name) + '"></div>',
        '      <div><span class="product-name">' + escapeHtml(product.product_name) + '</span><span class="sub-text">Giảm: ' + escapeHtml(product.discount_percent) + '% | Đánh giá: ' + escapeHtml(product.rating_avg) + '</span></div>',
        '    </div>',
        '  </td>',
        '  <td>' + escapeHtml(product.category_name || product.category_id) + '</td>',
        '  <td class="money-text">' + escapeHtml(formatMoney(product.unit_price || 0)) + '</td>',
        '  <td>' + escapeHtml(product.stock_quantity) + '</td>',
        '  <td>' + escapeHtml(product.sold_quantity || 0) + '</td>',
        '  <td><div class="row-actions"><button type="button" class="action-btn action-edit" data-action="edit-product" data-id="' + escapeHtml(product.product_id) + '">Sửa</button><button type="button" class="action-btn action-delete" data-action="delete-product" data-id="' + escapeHtml(product.product_id) + '">Xóa</button></div></td>',
        '</tr>'
      ].join('');
    }).join('') : renderEmptyRow(7, 'Không có sản phẩm phù hợp.');
  }

  function resetProductForm() {
    state.editingProductId = '';
    document.getElementById('productFormTitle').textContent = 'Thêm sản phẩm mới';
    document.getElementById('productSubmitBtn').textContent = 'Lưu sản phẩm';
    document.getElementById('productForm').reset();
    document.getElementById('productFormId').value = '';
    if (state.categories.length) {
      document.getElementById('productCategory').value = state.categories[0].category_id;
    }
  }

  function fillProductForm(productId) {
    var product = state.products.find(function (item) {
      return item.product_id === productId;
    });
    if (!product) {
      return;
    }

    state.editingProductId = product.product_id;
    document.getElementById('productFormTitle').textContent = 'Chỉnh sửa sản phẩm';
    document.getElementById('productSubmitBtn').textContent = 'Cập nhật sản phẩm';
    document.getElementById('productFormId').value = product.product_id;
    document.getElementById('productName').value = product.product_name || '';
    document.getElementById('productCategory').value = product.category_id || '';
    document.getElementById('productImageUrl').value = product.image_url || '';
    document.getElementById('productPrice').value = product.unit_price || 0;
    document.getElementById('productDiscount').value = product.discount_percent || 0;
    document.getElementById('productStock').value = product.stock_quantity || 0;
    document.getElementById('productRating').value = product.rating_avg || 0;
    document.getElementById('productReviews').value = product.total_reviews || 0;
    document.getElementById('productDescription').value = product.description || '';
  }

  function renderOrders() {
    document.getElementById('ordersMeta').textContent = state.orders.length + ' đơn';
    var body = document.getElementById('ordersTableBody');
    if (!body) {
      return;
    }

    body.innerHTML = state.orders.length ? state.orders.map(function (order) {
      var status = getStatusMeta(order.status);
      var options = ORDER_STATUSES.map(function (entry) {
        return '<option value="' + escapeHtml(entry) + '"' + (String(order.status || '').toLowerCase() === entry.toLowerCase() ? ' selected' : '') + '>' + escapeHtml(entry) + '</option>';
      }).join('');

      return [
        '<tr>',
        '  <td>' + escapeHtml(order.order_id) + '</td>',
        '  <td><span class="product-name">' + escapeHtml(order.customer_name || '-') + '</span><span class="sub-text">' + escapeHtml(order.customer_email || '-') + '</span></td>',
        '  <td class="money-text">' + escapeHtml(formatMoney(order.total_amount || 0)) + '</td>',
        '  <td>' + escapeHtml(formatDate(order.order_date)) + '</td>',
        '  <td><span class="status-chip ' + status.className + '">' + escapeHtml(status.label) + '</span></td>',
        '  <td><div class="inline-actions"><select class="status-select" data-order-status="' + escapeHtml(order.order_id) + '">' + options + '</select><button type="button" class="action-btn action-save" data-action="save-order-status" data-id="' + escapeHtml(order.order_id) + '">Lưu</button></div></td>',
        '</tr>'
      ].join('');
    }).join('') : renderEmptyRow(6, 'Không tìm thấy đơn hàng phù hợp.');
  }

  function renderCustomers() {
    document.getElementById('customersMeta').textContent = state.customers.length + ' tài khoản';
    populateDiscountTargets();

    var body = document.getElementById('customersTableBody');
    if (!body) {
      return;
    }

    body.innerHTML = state.customers.length ? state.customers.map(function (customer) {
      var isActive = Boolean(customer.is_active);
      return [
        '<tr>',
        '  <td>' + escapeHtml(customer.customer_id) + '</td>',
        '  <td><span class="product-name">' + escapeHtml(customer.customer_name) + '</span><span class="sub-text">Đơn gần nhất: ' + escapeHtml(formatDate(customer.last_order_date)) + '</span></td>',
        '  <td><span class="product-name">' + escapeHtml(customer.customer_email) + '</span><span class="sub-text">' + escapeHtml(customer.phone_number || '-') + '</span></td>',
        '  <td>' + escapeHtml(customer.orders_count || 0) + '</td>',
        '  <td class="money-text">' + escapeHtml(formatMoney(customer.total_spent || 0)) + '</td>',
        '  <td><span class="status-chip ' + (isActive ? 'status-success' : 'status-danger') + '">' + (isActive ? 'Hoạt động' : 'Tạm khóa') + '</span></td>',
        '  <td><div class="row-actions"><button type="button" class="action-btn action-edit" data-action="edit-customer" data-id="' + escapeHtml(customer.customer_id) + '">Sửa</button><button type="button" class="action-btn action-toggle" data-action="toggle-customer" data-id="' + escapeHtml(customer.customer_id) + '">' + (isActive ? 'Khóa' : 'Mở') + '</button></div></td>',
        '</tr>'
      ].join('');
    }).join('') : renderEmptyRow(7, 'Không tìm thấy tài khoản phù hợp.');
  }

  function resetCustomerForm() {
    state.editingCustomerId = '';
    document.getElementById('customerFormTitle').textContent = 'Chỉnh sửa người dùng';
    document.getElementById('customerForm').reset();
    document.getElementById('customerFormId').value = '';
    document.getElementById('customerStatus').value = '1';
  }

  function fillCustomerForm(customerId) {
    var customer = state.customers.find(function (item) {
      return item.customer_id === customerId;
    });
    if (!customer) {
      return;
    }

    state.editingCustomerId = customer.customer_id;
    document.getElementById('customerFormTitle').textContent = 'Cập nhật người dùng ' + customer.customer_id;
    document.getElementById('customerFormId').value = customer.customer_id;
    document.getElementById('customerName').value = customer.customer_name || '';
    document.getElementById('customerEmail').value = customer.customer_email || '';
    document.getElementById('customerPhone').value = customer.phone_number || '';
    document.getElementById('customerAddress').value = customer.address || '';
    document.getElementById('customerStatus').value = customer.is_active ? '1' : '0';
  }

  function renderDiscountCodes() {
    document.getElementById('discountsMeta').textContent = state.discountCodes.length + ' mã';
    var body = document.getElementById('discountsTableBody');
    if (!body) {
      return;
    }

    body.innerHTML = state.discountCodes.length ? state.discountCodes.map(function (discount) {
      return [
        '<tr>',
        '  <td><span class="product-name">' + escapeHtml(discount.code) + '</span><span class="sub-text">' + escapeHtml(discount.description || '-') + '</span></td>',
        '  <td>' + escapeHtml(discount.discount_percent) + '%</td>',
        '  <td>' + escapeHtml(discount.product_name || 'Tất cả sản phẩm') + '</td>',
        '  <td>' + escapeHtml(discount.customer_name || discount.customer_email || 'Tất cả người dùng') + '</td>',
        '  <td>' + escapeHtml(discount.used_count) + '/' + escapeHtml(discount.usage_limit) + '</td>',
        '  <td><span class="status-chip ' + (discount.is_active ? 'status-success' : 'status-danger') + '">' + (discount.is_active ? 'Đang bật' : 'Đang tắt') + '</span></td>',
        '  <td><div class="row-actions"><button type="button" class="action-btn action-edit" data-action="edit-discount" data-id="' + escapeHtml(discount.discount_code_id) + '">Sửa</button><button type="button" class="action-btn action-toggle" data-action="toggle-discount" data-id="' + escapeHtml(discount.discount_code_id) + '">' + (discount.is_active ? 'Tắt' : 'Bật') + '</button><button type="button" class="action-btn action-delete" data-action="delete-discount" data-id="' + escapeHtml(discount.discount_code_id) + '">Xóa</button></div></td>',
        '</tr>'
      ].join('');
    }).join('') : renderEmptyRow(7, 'Chưa có mã giảm giá nào.');
  }

  function resetDiscountForm() {
    state.editingDiscountId = '';
    document.getElementById('discountFormTitle').textContent = 'Tạo mã giảm giá';
    document.getElementById('discountSubmitBtn').textContent = 'Lưu mã giảm giá';
    document.getElementById('discountForm').reset();
    document.getElementById('discountFormId').value = '';
    document.getElementById('discountUsageLimit').value = 1;
    document.getElementById('discountStatus').value = 'true';
  }

  function fillDiscountForm(discountId) {
    var discount = state.discountCodes.find(function (item) {
      return item.discount_code_id === discountId;
    });
    if (!discount) {
      return;
    }

    state.editingDiscountId = discount.discount_code_id;
    document.getElementById('discountFormTitle').textContent = 'Cập nhật mã giảm giá';
    document.getElementById('discountSubmitBtn').textContent = 'Cập nhật mã';
    document.getElementById('discountFormId').value = discount.discount_code_id;
    document.getElementById('discountCode').value = discount.code || '';
    document.getElementById('discountPercent').value = discount.discount_percent || 1;
    document.getElementById('discountProduct').value = discount.product_id || '';
    document.getElementById('discountCustomer').value = discount.customer_id || '';
    document.getElementById('discountUsageLimit').value = discount.usage_limit || 1;
    document.getElementById('discountStartsAt').value = formatDateTimeLocal(discount.starts_at);
    document.getElementById('discountExpiresAt').value = formatDateTimeLocal(discount.expires_at);
    document.getElementById('discountStatus').value = discount.is_active ? 'true' : 'false';
    document.getElementById('discountDescription').value = discount.description || '';
  }

  async function loadCategories() {
    var response = await fetch(TamTai.API_BASE_URL + '/categories?skip=0&limit=100');
    var categories = await response.json();
    state.categories = Array.isArray(categories) ? categories : [];
    populateCategoryOptions();
  }

  async function loadDashboard() {
    state.dashboard = await request('/admin/dashboard');
    renderDashboard();
  }

  async function loadProducts() {
    var keyword = encodeURIComponent(normalizeSearchValue(document.getElementById('productSearch').value));
    var categoryId = encodeURIComponent(document.getElementById('productCategoryFilter').value || '');
    state.products = await request('/admin/products?skip=0&limit=300&keyword=' + keyword + '&category_id=' + categoryId);
    renderProducts();
  }

  async function loadOrders() {
    var keyword = encodeURIComponent(normalizeSearchValue(document.getElementById('orderSearch').value));
    state.orders = await request('/admin/orders?skip=0&limit=300&keyword=' + keyword);
    renderOrders();
  }

  async function loadCustomers() {
    var keyword = encodeURIComponent(normalizeSearchValue(document.getElementById('customerSearch').value));
    state.customers = await request('/admin/customers?skip=0&limit=300&keyword=' + keyword);
    renderCustomers();
  }

  async function loadDiscountCodes() {
    var keyword = encodeURIComponent(normalizeSearchValue(document.getElementById('discountSearch').value));
    state.discountCodes = await request('/admin/discount-codes?skip=0&limit=300&keyword=' + keyword);
    renderDiscountCodes();
  }

  async function refreshAll() {
    showMessage('Đang tải dữ liệu quản trị...', 'info');
    await loadCategories();
    await Promise.all([loadDashboard(), loadProducts(), loadOrders(), loadCustomers(), loadDiscountCodes()]);
    populateDiscountTargets();
    showMessage('Đã làm mới dữ liệu admin.', 'success');
  }

  async function saveProduct(event) {
    event.preventDefault();
    var payload = {
      product_name: document.getElementById('productName').value.trim(),
      category_id: document.getElementById('productCategory').value,
      image_url: document.getElementById('productImageUrl').value.trim() || null,
      unit_price: Number(document.getElementById('productPrice').value || 0),
      discount_percent: Number(document.getElementById('productDiscount').value || 0),
      stock_quantity: Number(document.getElementById('productStock').value || 0),
      rating_avg: Number(document.getElementById('productRating').value || 0),
      total_reviews: Number(document.getElementById('productReviews').value || 0),
      description: document.getElementById('productDescription').value.trim() || null
    };

    var editingId = document.getElementById('productFormId').value;
    await request(editingId ? '/admin/products/' + encodeURIComponent(editingId) : '/admin/products', {
      method: editingId ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    resetProductForm();
    await Promise.all([loadDashboard(), loadProducts(), loadDiscountCodes()]);
    showMessage(editingId ? 'Đã cập nhật sản phẩm.' : 'Đã thêm sản phẩm mới.', 'success');
  }

  async function updateCustomer(event) {
    event.preventDefault();
    var customerId = document.getElementById('customerFormId').value;
    if (!customerId) {
      showMessage('Hãy chọn một người dùng để chỉnh sửa.', 'info');
      return;
    }

    await request('/admin/customers/' + encodeURIComponent(customerId), {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_name: document.getElementById('customerName').value.trim(),
        customer_email: document.getElementById('customerEmail').value.trim(),
        phone_number: document.getElementById('customerPhone').value.trim() || null,
        address: document.getElementById('customerAddress').value.trim() || null,
        is_active: document.getElementById('customerStatus').value === '1'
      })
    });

    await Promise.all([loadCustomers(), loadDiscountCodes()]);
    showMessage('Đã cập nhật người dùng.', 'success');
  }

  async function saveDiscount(event) {
    event.preventDefault();
    var discountId = document.getElementById('discountFormId').value;
    var payload = {
      code: document.getElementById('discountCode').value.trim(),
      discount_percent: Number(document.getElementById('discountPercent').value || 0),
      product_id: document.getElementById('discountProduct').value || null,
      customer_id: document.getElementById('discountCustomer').value || null,
      usage_limit: Number(document.getElementById('discountUsageLimit').value || 1),
      starts_at: document.getElementById('discountStartsAt').value || null,
      expires_at: document.getElementById('discountExpiresAt').value || null,
      is_active: document.getElementById('discountStatus').value === 'true',
      description: document.getElementById('discountDescription').value.trim() || null
    };

    await request(discountId ? '/admin/discount-codes/' + encodeURIComponent(discountId) : '/admin/discount-codes', {
      method: discountId ? 'PATCH' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    resetDiscountForm();
    await Promise.all([loadDashboard(), loadDiscountCodes()]);
    showMessage(discountId ? 'Đã cập nhật mã giảm giá.' : 'Đã tạo mã giảm giá mới.', 'success');
  }

  async function handleProductTableClick(event) {
    var button = event.target.closest('button[data-action]');
    if (!button) {
      return;
    }

    var action = button.getAttribute('data-action');
    var id = button.getAttribute('data-id');

    if (action === 'edit-product') {
      fillProductForm(id);
      return;
    }

    if (action === 'delete-product') {
      if (!window.confirm('Bạn chắc chắn muốn xóa sản phẩm này?')) {
        return;
      }
      await request('/admin/products/' + encodeURIComponent(id), { method: 'DELETE' });
      await Promise.all([loadDashboard(), loadProducts(), loadDiscountCodes()]);
      showMessage('Đã xóa sản phẩm.', 'success');
    }
  }

  async function handleOrdersTableClick(event) {
    var button = event.target.closest('button[data-action="save-order-status"]');
    if (!button) {
      return;
    }

    var orderId = button.getAttribute('data-id');
    var select = document.querySelector('select[data-order-status="' + orderId + '"]');
    if (!select) {
      return;
    }

    await request('/admin/orders/' + encodeURIComponent(orderId) + '/status', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: select.value })
    });

    await Promise.all([loadDashboard(), loadOrders()]);
    showMessage('Đã cập nhật trạng thái đơn hàng.', 'success');
  }

  async function handleCustomersTableClick(event) {
    var button = event.target.closest('button[data-action]');
    if (!button) {
      return;
    }

    var action = button.getAttribute('data-action');
    var id = button.getAttribute('data-id');
    var customer = state.customers.find(function (item) { return item.customer_id === id; });
    if (!customer) {
      return;
    }

    if (action === 'edit-customer') {
      fillCustomerForm(id);
      return;
    }

    if (action === 'toggle-customer') {
      await request('/admin/customers/' + encodeURIComponent(id), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !customer.is_active })
      });
      await Promise.all([loadCustomers(), loadDiscountCodes()]);
      showMessage('Đã cập nhật trạng thái tài khoản.', 'success');
    }
  }

  async function handleDiscountsTableClick(event) {
    var button = event.target.closest('button[data-action]');
    if (!button) {
      return;
    }

    var action = button.getAttribute('data-action');
    var id = button.getAttribute('data-id');
    var discount = state.discountCodes.find(function (item) { return item.discount_code_id === id; });

    if (action === 'edit-discount') {
      fillDiscountForm(id);
      return;
    }

    if (action === 'toggle-discount' && discount) {
      await request('/admin/discount-codes/' + encodeURIComponent(id), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !discount.is_active })
      });
      await Promise.all([loadDashboard(), loadDiscountCodes()]);
      showMessage('Đã đổi trạng thái mã giảm giá.', 'success');
      return;
    }

    if (action === 'delete-discount') {
      if (!window.confirm('Bạn chắc chắn muốn xóa mã giảm giá này?')) {
        return;
      }
      await request('/admin/discount-codes/' + encodeURIComponent(id), { method: 'DELETE' });
      await Promise.all([loadDashboard(), loadDiscountCodes()]);
      showMessage('Đã xóa mã giảm giá.', 'success');
    }
  }

  function bindMenu() {
    document.querySelectorAll('.menu-link').forEach(function (button) {
      button.addEventListener('click', function () {
        setActiveView(button.getAttribute('data-view-target'));
        syncGlobalSearchFromView();
      });
    });
  }

  function bindSearches() {
    document.getElementById('productSearch').addEventListener('input', function () {
      loadProducts().catch(handleError);
    });
    document.getElementById('productCategoryFilter').addEventListener('change', function () {
      loadProducts().catch(handleError);
    });
    document.getElementById('orderSearch').addEventListener('input', function () {
      loadOrders().catch(handleError);
    });
    document.getElementById('customerSearch').addEventListener('input', function () {
      loadCustomers().catch(handleError);
    });
    document.getElementById('discountSearch').addEventListener('input', function () {
      loadDiscountCodes().catch(handleError);
    });
    document.getElementById('adminGlobalSearch').addEventListener('input', function () {
      var value = this.value;
      var mapping = {
        products: 'productSearch',
        orders: 'orderSearch',
        customers: 'customerSearch',
        discounts: 'discountSearch'
      };
      var target = mapping[state.currentView] ? document.getElementById(mapping[state.currentView]) : null;
      if (!target) {
        return;
      }
      target.value = value;
      target.dispatchEvent(new Event('input'));
    });
  }

  function bindButtons() {
    document.getElementById('refreshAllBtn').addEventListener('click', function () {
      refreshAll().catch(handleError);
    });
    document.getElementById('reloadProductsBtn').addEventListener('click', function () {
      loadProducts().catch(handleError);
    });
    document.getElementById('reloadOrdersBtn').addEventListener('click', function () {
      loadOrders().catch(handleError);
    });
    document.getElementById('reloadCustomersBtn').addEventListener('click', function () {
      loadCustomers().catch(handleError);
    });
    document.getElementById('reloadDiscountsBtn').addEventListener('click', function () {
      loadDiscountCodes().catch(handleError);
    });
    document.getElementById('resetProductFormBtn').addEventListener('click', resetProductForm);
    document.getElementById('productCancelBtn').addEventListener('click', resetProductForm);
    document.getElementById('resetCustomerFormBtn').addEventListener('click', resetCustomerForm);
    document.getElementById('customerCancelBtn').addEventListener('click', resetCustomerForm);
    document.getElementById('resetDiscountFormBtn').addEventListener('click', resetDiscountForm);
    document.getElementById('discountCancelBtn').addEventListener('click', resetDiscountForm);
  }

  function bindTables() {
    document.getElementById('productsTableBody').addEventListener('click', function (event) {
      handleProductTableClick(event).catch(handleError);
    });
    document.getElementById('ordersTableBody').addEventListener('click', function (event) {
      handleOrdersTableClick(event).catch(handleError);
    });
    document.getElementById('customersTableBody').addEventListener('click', function (event) {
      handleCustomersTableClick(event).catch(handleError);
    });
    document.getElementById('discountsTableBody').addEventListener('click', function (event) {
      handleDiscountsTableClick(event).catch(handleError);
    });
  }

  function bindForms() {
    document.getElementById('productForm').addEventListener('submit', function (event) {
      saveProduct(event).catch(handleError);
    });
    document.getElementById('customerForm').addEventListener('submit', function (event) {
      updateCustomer(event).catch(handleError);
    });
    document.getElementById('discountForm').addEventListener('submit', function (event) {
      saveDiscount(event).catch(handleError);
    });
  }

  function handleError(error) {
    showMessage((error && error.message) || 'Đã xảy ra lỗi khi làm việc với admin.', 'error');
  }

  document.addEventListener('DOMContentLoaded', async function () {
    document.body.style.visibility = 'hidden';
    var canAccess = await verifyAdminAccess();
    if (!canAccess) {
      return;
    }

    bindMenu();
    bindSearches();
    bindButtons();
    bindTables();
    bindForms();
    resetProductForm();
    resetCustomerForm();
    resetDiscountForm();

    try {
      await refreshAll();
      syncGlobalSearchFromView();
      document.body.style.visibility = 'visible';
    } catch (error) {
      document.body.style.visibility = 'visible';
      handleError(error);
    }
  });
})();
