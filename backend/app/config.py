import os
from pathlib import Path

from dotenv import load_dotenv

# Load biến môi trường từ backend/.env theo đường dẫn tuyệt đối
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL") or os.getenv("SMTP_USERNAME")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")
    EMAIL_OTP_TTL_MINUTES: int = int(os.getenv("EMAIL_OTP_TTL_MINUTES", "10"))
    EMAIL_OTP_MAX_ATTEMPTS: int = int(os.getenv("EMAIL_OTP_MAX_ATTEMPTS", "5"))
    EMAIL_OTP_RESEND_COOLDOWN_SECONDS: int = int(os.getenv("EMAIL_OTP_RESEND_COOLDOWN_SECONDS", "60"))
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@tamtai.vn")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() in ("1", "true", "yes")


settings = Settings()
