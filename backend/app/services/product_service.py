from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.exceptions import *


def get_product_by_id(db: Session, product_id: str):

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        raise NotFoundException("Product")

    return product


def get_all_products(db: Session, skip: int = 0, limit: int = 10):
    """Lấy tất cả products (có pagination)"""
    return db.query(Product).offset(skip).limit(limit).all()


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


def update_product(db: Session, product_id: str, data: ProductUpdate):
    """Cập nhật product"""
    product = get_product_by_id(db, product_id)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_id: str):

    product = get_product_by_id(db, product_id)

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
