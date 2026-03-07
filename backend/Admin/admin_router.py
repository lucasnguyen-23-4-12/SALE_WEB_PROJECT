from typing import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from Admin.admin_auth import authenticate_admin, create_access_token
from Admin.admin_schema import (
    AdminLoginRequest,
    AdminLoginResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from Admin import admin_service
from app.database import SessionLocal

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@router.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return admin_service.get_products(db)


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return admin_service.create_product(db, payload)


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db)
):
    updated_product = admin_service.update_product(db, product_id, payload)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return updated_product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = admin_service.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
