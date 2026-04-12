(function () {
  function detectCategory(item) {
    var icon = item.querySelector(".icon i");
    if (!icon) {
      return "system";
    }
    if (icon.classList.contains("fa-bag-shopping")) {
      return "orders";
    }
    if (icon.classList.contains("fa-ticket") || icon.classList.contains("fa-gift")) {
      return "promo";
    }
    return "system";
  }

  document.addEventListener("DOMContentLoaded", function () {
    TamTai.setupSearchRedirect(".search-box input", "../products/products.html");

    var items = Array.prototype.slice.call(document.querySelectorAll(".notify-item"));
    items.forEach(function (item) {
      item.setAttribute("data-category", detectCategory(item));
      item.addEventListener("click", function () {
        item.classList.remove("unread");
      });
    });

    var tabs = document.querySelectorAll(".notify-tabs button");
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (entry) { entry.classList.remove("active"); });
        tab.classList.add("active");

        var label = tab.textContent.trim().toLowerCase();
        var category = "all";
        if (label.indexOf("đơn hàng") !== -1) {
          category = "orders";
        } else if (label.indexOf("khuyến mãi") !== -1) {
          category = "promo";
        } else if (label.indexOf("hệ thống") !== -1) {
          category = "system";
        }

        items.forEach(function (item) {
          var byCategory = category === "all" || item.getAttribute("data-category") === category;
          item.style.display = byCategory ? "" : "none";
        });
      });
    });

    var markAllButton = document.querySelector(".notify-head button");
    if (markAllButton) {
      markAllButton.addEventListener("click", function () {
        items.forEach(function (item) {
          item.classList.remove("unread");
        });
      });
    }
  });
})();
