(function () {
  function togglePassword(btn) {
    var input = btn.parentElement.querySelector("input");
    var icon = btn.querySelector("i");
    if (!input || !icon) {
      return;
    }

    var showing = input.type === "text";
    input.type = showing ? "password" : "text";
    icon.classList.toggle("fa-eye", showing);
    icon.classList.toggle("fa-eye-slash", !showing);
  }

  async function loginAdmin(email, password, redirectTarget) {
    var formBody = new URLSearchParams();
    formBody.append("username", email);
    formBody.append("password", password);

    var adminResponse = await fetch(TamTai.API_BASE_URL + "/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formBody.toString()
    });

    var adminData = await adminResponse.json();
    if (!adminResponse.ok) {
      throw new Error(adminData.detail || "Admin login failed");
    }

    localStorage.setItem("access_token", adminData.access_token);
    localStorage.setItem("token_type", adminData.token_type || "bearer");
    localStorage.setItem("tamtai_role", "admin");
    window.location.href = redirectTarget === "admin" ? "../admin/admin.html" : "../admin/admin.html";
  }

  async function loginCustomer(email, password, redirectTarget) {
    var response = await fetch(TamTai.API_BASE_URL + "/customers/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email_or_phone: email,
        password: password
      })
    });

    var data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Login failed");
    }

    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("token_type", data.token_type || "bearer");
    localStorage.setItem("tamtai_role", "user");
    window.location.href = redirectTarget === "admin" ? "../admin/admin.html" : "../user/profile.html";
  }

  async function handleGoogleLogin(response) {
    try {
      var apiResponse = await fetch(TamTai.API_BASE_URL + "/customers/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_token: response.credential })
      });

      var data = await apiResponse.json();
      if (!apiResponse.ok) {
        throw new Error(data.detail || "Google login failed");
      }

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("token_type", data.token_type || "bearer");
      localStorage.setItem("tamtai_role", "user");
      window.location.href = "../user/profile.html";
    } catch (error) {
      alert(error.message || "Google sign-in failed. Please try again.");
    }
  }

  function initGoogleButton() {
    if (!window.google || !window.google.accounts || !window.google.accounts.id) {
      return;
    }

    var googleLoginBtn = document.getElementById("googleLoginBtn");
    if (!googleLoginBtn) {
      return;
    }

    google.accounts.id.initialize({
      client_id: TamTai.GOOGLE_CLIENT_ID,
      callback: handleGoogleLogin
    });

    google.accounts.id.renderButton(googleLoginBtn, {
      theme: "outline",
      size: "large",
      width: 320,
      text: "signin_with"
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    TamTai.setupSearchRedirect(".search-box input", "../products/products.html");

    document.querySelectorAll(".eye-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        togglePassword(btn);
      });
    });

    var form = document.getElementById("loginForm");
    var emailInput = document.getElementById("loginEmail");
    var passwordInput = document.getElementById("loginPassword");
    var redirectTarget = new URLSearchParams(window.location.search).get("redirect");

    if (form && emailInput && passwordInput) {
      form.addEventListener("submit", async function (event) {
        event.preventDefault();

        var email = emailInput.value.trim().toLowerCase();
        var password = passwordInput.value.trim();

        if (!email || !password) {
          alert("Vui lòng nhập email và mật khẩu.");
          return;
        }

        try {
          if (email === "admin@tamtai.vn") {
            await loginAdmin(email, password, redirectTarget);
          } else {
            await loginCustomer(email, password, redirectTarget);
          }
        } catch (error) {
          alert(error.message || "Đăng nhập thất bại.");
        }
      });
    }

    window.addEventListener("load", initGoogleButton);
  });
})();
