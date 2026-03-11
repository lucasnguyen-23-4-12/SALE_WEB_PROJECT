from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.payment_method import (
    PaymentMethodCreate,
    PaymentMethodUpdate,
    PaymentMethodResponse
)
from app.services import payment_service
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment Methods"]
)


@router.post(
    "/",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment_method(
    payload: PaymentMethodCreate,
    db: Session = Depends(get_db)
):
    return payment_service.create_payment_method(db, payload)


@router.get(
    "/",
    response_model=List[PaymentMethodResponse]
)
def get_payment_methods(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return payment_service.get_all_payment_methods(db, skip=skip, limit=limit)


@router.get(
    "/{payment_method_id}",
    response_model=PaymentMethodResponse
)
def get_payment_method(
    payment_method_id: str,
    db: Session = Depends(get_db)
):
    return payment_service.get_payment_method_by_id(db, payment_method_id)


@router.put(
    "/{payment_method_id}",
    response_model=PaymentMethodResponse
)
def update_payment_method(
    payment_method_id: str,
    payload: PaymentMethodUpdate,
    db: Session = Depends(get_db)
):
    return payment_service.update_payment_method(db, payment_method_id, payload)


@router.delete(
    "/{payment_method_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_payment_method(
    payment_method_id: str,
    db: Session = Depends(get_db)
):
    payment_service.delete_payment_method(db, payment_method_id)
