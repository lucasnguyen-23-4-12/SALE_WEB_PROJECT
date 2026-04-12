from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GoogleLoginRequest(BaseModel):
    id_token: str


class EmailOtpRequest(BaseModel):
    email: EmailStr


class ForgotPasswordVerifyOtpRequest(BaseModel):
    email: EmailStr
    otp_code: str


class ForgotPasswordVerifyOtpResponse(BaseModel):
    reset_token: str
    expires_in_minutes: int


class ForgotPasswordResetRequest(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str
