from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from threading import Lock
import hashlib
import random
import secrets
import smtplib

from app.config import settings
from app.services.exceptions import BusinessLogicException, ValidationException


_OTP_STORE: dict[str, dict] = {}
_RESET_TOKEN_STORE: dict[str, dict] = {}
_OTP_LOCK = Lock()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_email(email: str) -> str:
    normalized = (email or "").strip().lower()
    if not normalized:
        raise ValidationException("Email is required")
    return normalized


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def _cleanup_expired(now: datetime) -> None:
    expired_emails = [
        email
        for email, record in _OTP_STORE.items()
        if record["expires_at"] <= now
    ]
    for email in expired_emails:
        _OTP_STORE.pop(email, None)

    expired_tokens = [
        token
        for token, record in _RESET_TOKEN_STORE.items()
        if record["expires_at"] <= now
    ]
    for token in expired_tokens:
        _RESET_TOKEN_STORE.pop(token, None)


def _send_email_otp(receiver_email: str, code: str, ttl_minutes: int) -> None:
    if not settings.SMTP_HOST or not settings.SMTP_FROM_EMAIL:
        raise BusinessLogicException("SMTP is not configured")

    message = EmailMessage()
    message["Subject"] = "Your SALE_WEB verification code"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = receiver_email
    message.set_content(
        "Your verification code is: "
        f"{code}\n\n"
        f"This code expires in {ttl_minutes} minutes."
    )

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as smtp:
            if settings.SMTP_USE_TLS:
                smtp.starttls()
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            smtp.send_message(message)
    except Exception as exc:
        raise BusinessLogicException(f"Unable to send verification email: {exc}")


def request_email_otp(email: str) -> dict:
    normalized_email = _normalize_email(email)
    now = _utcnow()
    ttl_minutes = max(settings.EMAIL_OTP_TTL_MINUTES, 1)
    max_attempts = max(settings.EMAIL_OTP_MAX_ATTEMPTS, 1)
    resend_cooldown = max(settings.EMAIL_OTP_RESEND_COOLDOWN_SECONDS, 0)

    with _OTP_LOCK:
        _cleanup_expired(now)
        current = _OTP_STORE.get(normalized_email)
        if current and current["cooldown_until"] > now:
            wait_seconds = int((current["cooldown_until"] - now).total_seconds())
            raise BusinessLogicException(
                f"Please wait {wait_seconds} seconds before requesting a new code"
            )

        code = f"{random.SystemRandom().randint(0, 999999):06d}"
        _OTP_STORE[normalized_email] = {
            "code_hash": _hash_code(code),
            "expires_at": now + timedelta(minutes=ttl_minutes),
            "cooldown_until": now + timedelta(seconds=resend_cooldown),
            "attempts": 0,
            "max_attempts": max_attempts,
        }

    try:
        _send_email_otp(normalized_email, code, ttl_minutes)
    except Exception:
        with _OTP_LOCK:
            _OTP_STORE.pop(normalized_email, None)
        raise

    return {
        "message": "Verification code sent",
        "expires_in_minutes": ttl_minutes,
        "resend_after_seconds": resend_cooldown,
    }


def verify_and_consume_email_otp(email: str, code: str) -> None:
    normalized_email = _normalize_email(email)
    sanitized_code = (code or "").strip()
    if not sanitized_code.isdigit() or len(sanitized_code) != 6:
        raise ValidationException("OTP must be a 6-digit code")

    now = _utcnow()
    with _OTP_LOCK:
        _cleanup_expired(now)
        record = _OTP_STORE.get(normalized_email)
        if not record:
            raise ValidationException("OTP not found or expired")

        if record["attempts"] >= record["max_attempts"]:
            _OTP_STORE.pop(normalized_email, None)
            raise ValidationException("OTP has been locked. Please request a new code")

        if record["code_hash"] != _hash_code(sanitized_code):
            record["attempts"] += 1
            if record["attempts"] >= record["max_attempts"]:
                _OTP_STORE.pop(normalized_email, None)
            raise ValidationException("Invalid OTP")

        _OTP_STORE.pop(normalized_email, None)


def verify_email_otp_and_create_reset_token(email: str, code: str) -> dict:
    normalized_email = _normalize_email(email)
    verify_and_consume_email_otp(normalized_email, code)

    now = _utcnow()
    ttl_minutes = max(settings.EMAIL_OTP_TTL_MINUTES, 1)
    token = secrets.token_urlsafe(32)

    with _OTP_LOCK:
        _cleanup_expired(now)
        _RESET_TOKEN_STORE[token] = {
            "email": normalized_email,
            "expires_at": now + timedelta(minutes=ttl_minutes),
        }

    return {
        "reset_token": token,
        "expires_in_minutes": ttl_minutes,
    }


def consume_password_reset_token(email: str, reset_token: str) -> None:
    normalized_email = _normalize_email(email)
    sanitized_token = (reset_token or "").strip()
    if not sanitized_token:
        raise ValidationException("Reset token is required")

    now = _utcnow()
    with _OTP_LOCK:
        _cleanup_expired(now)
        record = _RESET_TOKEN_STORE.get(sanitized_token)
        if not record:
            raise ValidationException("Reset token is invalid or expired")

        if record["email"] != normalized_email:
            _RESET_TOKEN_STORE.pop(sanitized_token, None)
            raise ValidationException("Reset token does not match this email")

        _RESET_TOKEN_STORE.pop(sanitized_token, None)
