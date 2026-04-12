from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from Admin import admin_service
from Admin.admin_auth import authenticate_admin, create_access_token, get_current_admin
from Admin.admin_schema import (
    AdminCustomerResponse,
    AdminCustomerUpdate,
    AdminDashboardResponse,
    AdminLoginResponse,
    AdminOrderResponse,
    AdminProductCreate,
    AdminProductResponse,
    AdminProductUpdate,
    DiscountCodeCreate,
    DiscountCodeResponse,
    DiscountCodeUpdate,
)
from app.core.dependencies import get_db
from app.schemas.order import OrderUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    is_valid = authenticate_admin(form_data.username, form_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin username or password",
        )

    access_token = create_access_token({"sub": form_data.username})
    return AdminLoginResponse(access_token=access_token, token_type="bearer")


@router.get("/me")
def admin_me(admin: str = Depends(get_current_admin)):
    return {"username": admin, "role": "admin"}


@router.get("/dashboard", response_model=AdminDashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_dashboard(db)


@router.get("/products", response_model=list[AdminProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=300),
    keyword: str | None = Query(default=None),
    category_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_products(
        db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        category_id=category_id,
    )


@router.get("/products/{product_id}", response_model=AdminProductResponse)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_product_by_id(db, product_id)


@router.post(
    "/products",
    response_model=AdminProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: AdminProductCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.create_product(db, payload)


@router.put("/products/{product_id}", response_model=AdminProductResponse)
def update_product(
    product_id: str,
    payload: AdminProductUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.update_product(db, product_id, payload)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    admin_service.delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/orders", response_model=list[AdminOrderResponse])
def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=300),
    keyword: str | None = Query(default=None),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_orders(db, skip=skip, limit=limit, keyword=keyword)


@router.get("/orders/{order_id}", response_model=AdminOrderResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_order_by_id(db, order_id)


@router.patch("/orders/{order_id}/status", response_model=AdminOrderResponse)
def update_order_status(
    order_id: str,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.update_order_status(db, order_id, payload)


@router.get("/customers", response_model=list[AdminCustomerResponse])
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=300),
    keyword: str | None = Query(default=None),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_customers(db, skip=skip, limit=limit, keyword=keyword)


@router.get("/customers/{customer_id}", response_model=AdminCustomerResponse)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_customer_by_id(db, customer_id)


@router.patch("/customers/{customer_id}", response_model=AdminCustomerResponse)
def update_customer(
    customer_id: str,
    payload: AdminCustomerUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.update_customer(db, customer_id, payload)


@router.get("/discount-codes", response_model=list[DiscountCodeResponse])
def get_discount_codes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=300),
    keyword: str | None = Query(default=None),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_discount_codes(db, skip=skip, limit=limit, keyword=keyword)


@router.post(
    "/discount-codes",
    response_model=DiscountCodeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_discount_code(
    payload: DiscountCodeCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.create_discount_code(db, payload)


@router.patch("/discount-codes/{discount_code_id}", response_model=DiscountCodeResponse)
def update_discount_code(
    discount_code_id: str,
    payload: DiscountCodeUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.update_discount_code(db, discount_code_id, payload)


@router.delete(
    "/discount-codes/{discount_code_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_discount_code(
    discount_code_id: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    admin_service.delete_discount_code(db, discount_code_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
