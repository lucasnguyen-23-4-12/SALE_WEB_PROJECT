from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerLogin
)
from app.schemas.auth import TokenResponse
from app.services import customer_service
from app.core.customer_auth import create_customer_access_token, get_current_customer
from app.core.dependencies import get_db
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
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
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
    customer_id: int,
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
    customer_id: int,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if current_customer.customer_id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    customer_service.delete_customer(db, customer_id)
