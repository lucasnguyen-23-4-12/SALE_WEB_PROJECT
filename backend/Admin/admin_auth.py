from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = settings.SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login",
    scheme_name="AdminOAuth2PasswordBearer",
)


def _normalize_admin_identifier(value: str) -> str:
    return (value or "").strip().lower()


ADMIN_IDENTIFIERS = {
    normalized
    for normalized in {
        _normalize_admin_identifier(settings.ADMIN_USERNAME),
        _normalize_admin_identifier(settings.ADMIN_EMAIL),
    }
    if normalized
}
ADMIN_PASSWORD = settings.ADMIN_PASSWORD


def authenticate_admin(username: str, password: str) -> bool:
    normalized_username = _normalize_admin_identifier(username)
    return normalized_username in ADMIN_IDENTIFIERS and password == ADMIN_PASSWORD


def create_access_token(data: dict) -> str:
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in environment variables.")

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_admin(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        normalized_username = _normalize_admin_identifier(username)
        if not normalized_username:
            raise credentials_exception
        if normalized_username not in ADMIN_IDENTIFIERS:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return username
