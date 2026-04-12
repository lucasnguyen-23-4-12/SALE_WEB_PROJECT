from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.wishlist import WishlistCreate, WishlistResponse
from app.services import wishlist_service
from app.core.customer_auth import get_current_customer
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/wishlists",
    tags=["Wishlists"]
)

@router.post("/", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    payload: WishlistCreate,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if payload.customer_id != current_customer.customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return wishlist_service.add_item(db, payload)

@router.get("/customer/{customer_id}", response_model=List[WishlistResponse])
def get_wishlist(
    customer_id: str,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    if customer_id != current_customer.customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return wishlist_service.get_by_customer(db, customer_id)

@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(
    wishlist_id: str,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    item = wishlist_service.get_item(db, wishlist_id)
    if item.customer_id != current_customer.customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    wishlist_service.remove_item(db, wishlist_id)
