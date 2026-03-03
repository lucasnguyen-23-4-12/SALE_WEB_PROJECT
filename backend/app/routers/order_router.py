from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.order import (
    OrderCreate,
    OrderResponse
)
from app.services import order_service
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.create_order(db, payload)


@router.get(
    "/",
    response_model=List[OrderResponse]
)
def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return order_service.get_all_orders(db, skip=skip, limit=limit)


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return order_service.get_order_by_id(db, order_id)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order_service.delete_order(db, order_id)