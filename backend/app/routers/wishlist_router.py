from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.wishlist import WishlistCreate, WishlistResponse
from app.services import wishlist_service
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/wishlists",
    tags=["Wishlists"]
)

@router.post("/", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(payload: WishlistCreate, db: Session = Depends(get_db)):
    return wishlist_service.add_item(db, payload)

@router.get("/customer/{customer_id}", response_model=List[WishlistResponse])
def get_wishlist(customer_id: int, db: Session = Depends(get_db)):
    return wishlist_service.get_by_customer(db, customer_id)

@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(wishlist_id: int, db: Session = Depends(get_db)):
    wishlist_service.remove_item(db, wishlist_id)