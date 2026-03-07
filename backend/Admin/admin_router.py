from fastapi import APIRouter, HTTPException, status

from Admin.admin_auth import authenticate_admin, create_access_token
from Admin.admin_schema import AdminLoginRequest, AdminLoginResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(payload: AdminLoginRequest):
    is_valid = authenticate_admin(payload.username, payload.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin username or password",
        )

    access_token = create_access_token({"sub": payload.username})
    return AdminLoginResponse(access_token=access_token, token_type="bearer")
