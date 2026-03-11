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

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def authenticate_admin(username: str, password: str) -> bool:
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD


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
        if username is None:
            raise credentials_exception
        if username != ADMIN_USERNAME:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return username
