from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate
from app.services.exceptions import *


def get_product_by_id(db: Session, product_id: int):

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        raise NotFoundException("Product")

    return product


def create_product(db: Session, data: ProductCreate):

    category = db.query(Category).filter(
        Category.category_id == data.category_id
    ).first()

    if not category:
        raise NotFoundException("Category")

    new_product = Product(**data.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()


def delete_product(db: Session, product_id: int):

    product = get_product_by_id(db, product_id)

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}