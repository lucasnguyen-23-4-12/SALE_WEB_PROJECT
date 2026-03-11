from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from Admin.admin_auth import authenticate_admin, create_access_token, get_current_admin
from Admin.admin_schema import AdminLoginResponse
from Admin import admin_service
from app.core.dependencies import get_db
from app.schemas.order import OrderResponse, OrderUpdate
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

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


@router.get("/products", response_model=list[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_products(db, skip=skip, limit=limit)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_product_by_id(db, product_id)


@router.get("/orders", response_model=list[OrderResponse])
def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_orders(db, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.get_order_by_id(db, order_id)


@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.update_order_status(db, order_id, payload)


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.create_product(db, payload)


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return admin_service.update_product(db, product_id, payload)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    admin_service.delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
