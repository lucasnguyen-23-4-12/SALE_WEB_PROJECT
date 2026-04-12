from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from app.schemas.customer import (
    CustomerCreate,
    CustomerRegisterWithOtp,
    CustomerUpdate,
    CustomerResponse,
    CustomerLogin,
    CustomerChangePassword
)
from app.schemas.auth import (
    TokenResponse,
    GoogleLoginRequest,
    EmailOtpRequest,
    ForgotPasswordVerifyOtpRequest,
    ForgotPasswordVerifyOtpResponse,
    ForgotPasswordResetRequest,
)
from app.services import customer_service, email_otp_service
from app.core.customer_auth import create_customer_access_token, get_current_customer
from app.core.dependencies import get_db
from app.config import settings
from Admin.admin_auth import get_current_admin

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db)
):
    return customer_service.create_customer(db, payload)


@router.post(
    "/register/request-otp",
    status_code=status.HTTP_202_ACCEPTED
)
def request_register_otp(payload: EmailOtpRequest):
    return email_otp_service.request_email_otp(payload.email)


@router.post(
    "/forgot-password/request-otp",
    status_code=status.HTTP_202_ACCEPTED
)
def request_forgot_password_otp(
    payload: EmailOtpRequest,
    db: Session = Depends(get_db)
):
    customer_service.get_customer_by_email(db, str(payload.email))
    return email_otp_service.request_email_otp(payload.email)


@router.post(
    "/forgot-password/verify-otp",
    response_model=ForgotPasswordVerifyOtpResponse
)
def verify_forgot_password_otp(
    payload: ForgotPasswordVerifyOtpRequest,
    db: Session = Depends(get_db)
):
    customer_service.get_customer_by_email(db, str(payload.email))
    return email_otp_service.verify_email_otp_and_create_reset_token(
        email=str(payload.email),
        code=payload.otp_code
    )


@router.post(
    "/forgot-password/reset"
)
def reset_forgot_password(
    payload: ForgotPasswordResetRequest,
    db: Session = Depends(get_db)
):
    email_otp_service.consume_password_reset_token(
        email=str(payload.email),
        reset_token=payload.reset_token
    )
    return customer_service.reset_customer_password_by_email(
        db=db,
        email=str(payload.email),
        new_password=payload.new_password
    )


@router.post(
    "/register/with-otp",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer_with_otp(
    payload: CustomerRegisterWithOtp,
    db: Session = Depends(get_db)
):
    email_otp_service.verify_and_consume_email_otp(
        email=str(payload.customer_email),
        code=payload.otp_code
    )
    customer_data = payload.model_dump(exclude={"otp_code"})
    customer_data["customer_email"] = customer_data["customer_email"].strip().lower()
    return customer_service.create_customer(db, CustomerCreate(**customer_data))


@router.post(
    "/login",
    response_model=TokenResponse
)
def login_customer(
    payload: CustomerLogin,
    db: Session = Depends(get_db)
):
    customer = customer_service.authenticate_customer(
        db, payload.email_or_phone, payload.password
    )
    token = create_customer_access_token(customer.customer_id)
    return TokenResponse(access_token=token)


@router.post(
    "/google",
    response_model=TokenResponse
)
def login_customer_with_google(
    payload: GoogleLoginRequest,
    db: Session = Depends(get_db)
):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth is not configured"
        )

    try:
        token_info = google_id_token.verify_oauth2_token(
            payload.id_token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(exc)}"
        )

    email = (token_info.get("email") or "").strip().lower()
    name = (token_info.get("name") or "").strip()
    email_verified = bool(token_info.get("email_verified"))

    if not email or not email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account email is not verified"
        )

    customer = customer_service.get_or_create_google_customer(
        db=db,
        email=email,
        name=name
    )
    token = create_customer_access_token(customer.customer_id)
    return TokenResponse(access_token=token)


@router.post(
    "/token",
    response_model=TokenResponse,
)
def token_customer(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    customer = customer_service.authenticate_customer(
        db, form_data.username, form_data.password
    )
    token = create_customer_access_token(customer.customer_id)
    return TokenResponse(access_token=token)


@router.get(
    "/",
    response_model=List[CustomerResponse]
)
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return customer_service.get_all_customers(db, skip=skip, limit=limit)


@router.get(
    "/me",
    response_model=CustomerResponse
)
def get_my_profile(
    current_customer=Depends(get_current_customer),
):
    return current_customer


@router.post(
    "/change-password"
)
def change_my_password(
    payload: CustomerChangePassword,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    return customer_service.change_customer_password(
        db=db,
        customer_id=current_customer.customer_id,
        current_password=payload.current_password,
        new_password=payload.new_password
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if current_customer.customer_id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return customer_service.get_customer_by_id(db, customer_id)


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: str,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if current_customer.customer_id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return customer_service.update_customer(db, customer_id, payload)


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if current_customer.customer_id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    customer_service.delete_customer(db, customer_id)
