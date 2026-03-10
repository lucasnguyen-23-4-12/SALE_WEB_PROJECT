from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate
from app.services.exceptions import NotFoundException


def add_item(db: Session, data: WishlistCreate):
    item = Wishlist(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_by_customer(db: Session, customer_id: int):
    return db.query(Wishlist).filter(Wishlist.customer_id == customer_id).all()


def get_item(db: Session, wishlist_id: int):
    item = db.query(Wishlist).filter(Wishlist.wishlist_id == wishlist_id).first()
    if not item:
        raise NotFoundException("Wishlist item")
    return item


def remove_item(db: Session, wishlist_id: int):
    item = get_item(db, wishlist_id)
    db.delete(item)
    db.commit()
    return {"message": "Removed"}