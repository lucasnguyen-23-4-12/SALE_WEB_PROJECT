(function () {
  var otpCooldownTimer = null;
  var state = {
    verifiedEmail: "",
    resetToken: ""
  };

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

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function setStatus(textEl, message, isError) {
    if (!textEl) {
      return;
    }
    textEl.textContent = message;
    textEl.style.color = isError ? "#cc3d3d" : "#4d8f49";
  }

  function disablePasswordFields(disabled) {
    var newPasswordInput = document.getElementById("forgotNewPassword");
    var confirmPasswordInput = document.getElementById("forgotConfirmPassword");
    var submitBtn = document.getElementById("forgotSubmitBtn");

    if (newPasswordInput) {
      newPasswordInput.disabled = disabled;
      if (disabled) {
        newPasswordInput.value = "";
      }
    }
    if (confirmPasswordInput) {
      confirmPasswordInput.disabled = disabled;
      if (disabled) {
        confirmPasswordInput.value = "";
      }
    }
    if (submitBtn) {
      submitBtn.disabled = disabled;
    }
  }

  function clearVerificationState() {
    state.verifiedEmail = "";
    state.resetToken = "";
    disablePasswordFields(true);
  }

  function startOtpCooldown(button, seconds) {
    var remaining = Number(seconds || 60);
    button.disabled = true;
    button.textContent = "Gui lai (" + remaining + "s)";

    if (otpCooldownTimer) {
      clearInterval(otpCooldownTimer);
    }

    otpCooldownTimer = setInterval(function () {
      remaining -= 1;
      if (remaining <= 0) {
        clearInterval(otpCooldownTimer);
        otpCooldownTimer = null;
        button.disabled = false;
        button.textContent = "Gửi mã";
        return;
      }
      button.textContent = "Gui lai (" + remaining + "s)";
    }, 1000);
  }

  async function requestOtp(email, sendOtpBtn, statusEl) {
    var response = await fetch(TamTai.API_BASE_URL + "/customers/forgot-password/request-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email })
    });

    var data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Khong gui duoc OTP.");
    }

    var ttl = data.expires_in_minutes || 10;
    var cooldown = data.resend_after_seconds || 60;
    setStatus(statusEl, "OTP da gui toi " + email + ". Hieu luc " + ttl + " phut.", false);
    startOtpCooldown(sendOtpBtn, cooldown);
  }

  async function verifyOtp(email, otpCode) {
    var response = await fetch(TamTai.API_BASE_URL + "/customers/forgot-password/verify-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email,
        otp_code: otpCode
      })
    });

    var data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "OTP khong hop le.");
    }

    return data;
  }

  async function resetPassword(email, resetToken, newPassword) {
    var response = await fetch(TamTai.API_BASE_URL + "/customers/forgot-password/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email,
        reset_token: resetToken,
        new_password: newPassword
      })
    });

    var data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Khong cap nhat duoc mat khau.");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    TamTai.setupSearchRedirect(".search-box input", "../products/products.html");

    var form = document.getElementById("forgotPasswordForm");
    var emailInput = document.getElementById("forgotEmail");
    var otpInput = document.getElementById("forgotOtp");
    var sendOtpBtn = document.getElementById("forgotSendOtpBtn");
    var verifyOtpBtn = document.getElementById("forgotVerifyOtpBtn");
    var statusEl = document.getElementById("forgotOtpStatusText");
    var newPasswordInput = document.getElementById("forgotNewPassword");
    var confirmPasswordInput = document.getElementById("forgotConfirmPassword");

    document.querySelectorAll(".eye-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        togglePassword(btn);
      });
    });

    clearVerificationState();

    if (!form || !emailInput || !otpInput || !sendOtpBtn || !verifyOtpBtn || !statusEl || !newPasswordInput || !confirmPasswordInput) {
      return;
    }

    emailInput.addEventListener("input", function () {
      clearVerificationState();
      setStatus(statusEl, "Mã OTP có hiệu lực 10 phút.", false);
    });

    otpInput.addEventListener("input", function () {
      clearVerificationState();
      setStatus(statusEl, "Mã OTP có hiệu lực 10 phút.", false);
    });

    sendOtpBtn.addEventListener("click", async function () {
      var email = emailInput.value.trim().toLowerCase();
      clearVerificationState();

      if (!isValidEmail(email)) {
        setStatus(statusEl, "Vui long nhap email hop le.", true);
        return;
      }

      sendOtpBtn.disabled = true;
      try {
        await requestOtp(email, sendOtpBtn, statusEl);
      } catch (error) {
        sendOtpBtn.disabled = false;
        setStatus(statusEl, error.message || "Khong gui duoc OTP.", true);
      }
    });

    verifyOtpBtn.addEventListener("click", async function () {
      var email = emailInput.value.trim().toLowerCase();
      var otpCode = otpInput.value.trim();
      clearVerificationState();

      if (!isValidEmail(email)) {
        setStatus(statusEl, "Vui long nhap email hop le.", true);
        return;
      }
      if (!/^\d{6}$/.test(otpCode)) {
        setStatus(statusEl, "OTP phai gom dung 6 chu so.", true);
        return;
      }

      verifyOtpBtn.disabled = true;
      try {
        var payload = await verifyOtp(email, otpCode);
        state.verifiedEmail = email;
        state.resetToken = payload.reset_token || "";
        disablePasswordFields(false);
        setStatus(statusEl, "Xac minh OTP thanh cong. Ban co the dat mat khau moi.", false);
      } catch (error) {
        setStatus(statusEl, error.message || "OTP khong hop le.", true);
      } finally {
        verifyOtpBtn.disabled = false;
      }
    });

    form.addEventListener("submit", async function (event) {
      event.preventDefault();

      var email = emailInput.value.trim().toLowerCase();
      var password = newPasswordInput.value.trim();
      var confirm = confirmPasswordInput.value.trim();

      if (!state.resetToken || state.verifiedEmail !== email) {
        alert("Ban can xac minh OTP dung email truoc khi dat mat khau moi.");
        return;
      }

      if (password.length < 6) {
        alert("Mat khau moi toi thieu 6 ky tu.");
        return;
      }

      if (password !== confirm) {
        alert("Mat khau xac nhan chua khop.");
        return;
      }

      var submitBtn = document.getElementById("forgotSubmitBtn");
      if (submitBtn) {
        submitBtn.disabled = true;
      }

      try {
        await resetPassword(email, state.resetToken, password);
        alert("Cap nhat mat khau thanh cong. Vui long dang nhap lai.");
        window.location.href = "login.html";
      } catch (error) {
        alert(error.message || "Khong cap nhat duoc mat khau.");
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
        }
      }
    });
  });
})();
