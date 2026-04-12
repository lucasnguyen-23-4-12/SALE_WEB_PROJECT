(function () {
  var otpCooldownTimer = null;

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

  function setOtpStatus(textEl, message, isError) {
    if (!textEl) {
      return;
    }
    textEl.textContent = message;
    textEl.style.color = isError ? "#cc3d3d" : "#4d8f49";
  }

  function startOtpCooldown(button, seconds) {
    var remaining = Number(seconds || 60);
    button.disabled = true;
    button.textContent = "Resend (" + remaining + "s)";

    if (otpCooldownTimer) {
      clearInterval(otpCooldownTimer);
    }

    otpCooldownTimer = setInterval(function () {
      remaining -= 1;
      if (remaining <= 0) {
        clearInterval(otpCooldownTimer);
        otpCooldownTimer = null;
        button.disabled = false;
        button.textContent = "Send code";
        return;
      }
      button.textContent = "Resend (" + remaining + "s)";
    }, 1000);
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  async function sendOtp(email, sendOtpBtn, otpStatusText) {
    var response = await fetch(TamTai.API_BASE_URL + "/customers/register/request-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email })
    });

    var data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to send OTP code");
    }

    var ttl = data.expires_in_minutes || 10;
    var cooldown = data.resend_after_seconds || 60;
    setOtpStatus(otpStatusText, "OTP đã gửi tới " + email + ". Mã hết hạn sau " + ttl + " phút.", false);
    startOtpCooldown(sendOtpBtn, cooldown);
  }

  async function registerWithOtp(payload) {
    var response = await fetch(TamTai.API_BASE_URL + "/customers/register/with-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    var data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Registration failed");
    }
  }

  async function handleGoogleRegister(response) {
    try {
      var apiResponse = await fetch(TamTai.API_BASE_URL + "/customers/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_token: response.credential })
      });

      var data = await apiResponse.json();
      if (!apiResponse.ok) {
        throw new Error(data.detail || "Google register failed");
      }

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("token_type", data.token_type || "bearer");
      localStorage.setItem("tamtai_role", "user");
      window.location.href = "../user/profile.html";
    } catch (error) {
          alert(error.message || "Đăng ký thất bại.");
    }
  }

  function initGoogleButton() {
    if (!window.google || !window.google.accounts || !window.google.accounts.id) {
      return;
    }

    var googleRegisterBtn = document.getElementById("googleRegisterBtn");
    if (!googleRegisterBtn) {
      return;
    }

    google.accounts.id.initialize({
      client_id: TamTai.GOOGLE_CLIENT_ID,
      callback: handleGoogleRegister
    });

    google.accounts.id.renderButton(googleRegisterBtn, {
      theme: "outline",
      size: "large",
      width: 320,
      text: "signup_with"
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    TamTai.setupSearchRedirect(".search-box input", "../products/products.html");

    var form = document.getElementById("registerForm");
    var registerName = document.getElementById("registerName");
    var registerEmail = document.getElementById("registerEmail");
    var registerOtp = document.getElementById("registerOtp");
    var registerPassword = document.getElementById("registerPassword");
    var registerConfirmPassword = document.getElementById("registerConfirmPassword");
    var sendOtpBtn = document.getElementById("sendOtpBtn");
    var otpStatusText = document.getElementById("otpStatusText");

    document.querySelectorAll(".eye-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        togglePassword(btn);
      });
    });

    if (sendOtpBtn && registerEmail) {
      sendOtpBtn.addEventListener("click", async function () {
        var email = registerEmail.value.trim().toLowerCase();
        if (!isValidEmail(email)) {
          setOtpStatus(otpStatusText, "Email không hợp lệ.", true);
          return;
        }

        sendOtpBtn.disabled = true;
        try {
          await sendOtp(email, sendOtpBtn, otpStatusText);
        } catch (error) {
          sendOtpBtn.disabled = false;
          setOtpStatus(otpStatusText, error.message || "Không gửi được OTP.", true);
        }
      });
    }

    if (form) {
      form.addEventListener("submit", async function (event) {
        event.preventDefault();

        var customer_name = registerName.value.trim();
        var customer_email = registerEmail.value.trim().toLowerCase();
        var otp_code = registerOtp.value.trim();
        var password = registerPassword.value;
        var confirmPassword = registerConfirmPassword.value;

        if (!customer_name || !customer_email || !password || !confirmPassword || !otp_code) {
          alert("Vui lòng điền đủ thông tin và mã OTP.");
          return;
        }

        if (!isValidEmail(customer_email)) {
          alert("Email không hợp lệ.");
          return;
        }

        if (!/^\d{6}$/.test(otp_code)) {
          alert("OTP phải gồm đúng 6 chữ số.");
          return;
        }

        if (password.length < 6) {
          alert("Mật khẩu tối thiểu 6 ký tự.");
          return;
        }

        if (password !== confirmPassword) {
          alert("Mật khẩu xác nhận chưa khớp.");
          return;
        }

        try {
          await registerWithOtp({
            customer_name: customer_name,
            customer_email: customer_email,
            password: password,
            otp_code: otp_code
          });

          alert("Đăng ký thành công. Bạn có thể đăng nhập ngay.");
          window.location.href = "login.html";
        } catch (error) {
          alert(error.message || "Đăng ký thất bại.");
        }
      });
    }

    window.addEventListener("load", initGoogleButton);
  });
})();

