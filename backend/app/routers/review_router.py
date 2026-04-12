from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.review import ReviewCreate, ReviewResponse
from app.services import review_service
from app.core.customer_auth import get_current_customer
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if payload.customer_id != current_customer.customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return review_service.create_review(db, payload)

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def reviews_by_product(product_id: str, db: Session = Depends(get_db)):
    return review_service.get_reviews_by_product(db, product_id)

@router.get("/customer/{customer_id}", response_model=List[ReviewResponse])
def reviews_by_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if customer_id != current_customer.customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return review_service.get_reviews_by_customer(db, customer_id)
