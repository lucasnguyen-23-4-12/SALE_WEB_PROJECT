from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.review import Review
from app.schemas.review import ReviewCreate
from datetime import datetime
from app.services.exceptions import NotFoundException


def create_review(db: Session, data: ReviewCreate):
    existing = db.query(Review).filter(
        Review.product_id == data.product_id,
        Review.customer_id == data.customer_id
    ).first()

    if existing:
        existing.rating = data.rating
        existing.comment = data.comment
        existing.created_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        review_record = existing
    else:
        new = Review(**data.model_dump())
        new.created_at = datetime.utcnow()
        db.add(new)
        db.commit()
        db.refresh(new)
        review_record = new

    # update product aggregates
    total = db.query(Review).filter(Review.product_id == review_record.product_id).count()
    sum_rating = db.query(func.sum(Review.rating)).filter(Review.product_id == review_record.product_id).scalar() or 0
    avg = float(sum_rating) / total if total > 0 else 0.0
    from app.models.product import Product
    prod = db.query(Product).get(review_record.product_id)
    if prod:
        prod.total_reviews = total
        prod.rating_avg = avg
        db.commit()
        db.refresh(prod)

    return review_record


def get_reviews_by_product(db: Session, product_id: str):
    return db.query(Review).filter(Review.product_id == product_id).all()


def get_reviews_by_customer(db: Session, customer_id: str):
    return db.query(Review).filter(Review.customer_id == customer_id).all()


def get_review_by_id(db: Session, review_id: str):
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise NotFoundException("Review")
    return review


def delete_review(db: Session, review_id: str):
    review = get_review_by_id(db, review_id)
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}
