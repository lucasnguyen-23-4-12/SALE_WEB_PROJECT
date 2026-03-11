from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.core.dependencies import get_db
from app.models.customer import Customer

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = settings.SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/customers/login")


def create_customer_access_token(customer_id: int) -> str:
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in environment variables.")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(customer_id), "role": "customer", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_customer(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Customer:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        role = payload.get("role")
        if not sub or role != "customer":
            raise credentials_exception
        customer_id = int(sub)
    except (JWTError, ValueError):
        raise credentials_exception

    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise credentials_exception

    return customer

