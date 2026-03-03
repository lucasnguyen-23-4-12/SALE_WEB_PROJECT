from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.exceptions import *


def get_category_by_id(db: Session, category_id: int):
    """Lấy category theo ID"""
    category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if not category:
        raise NotFoundException("Category")

    return category


def get_all_categories(db: Session, skip: int = 0, limit: int = 10):
    """Lấy tất cả categories (có pagination)"""
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, data: CategoryCreate):
    """Tạo category mới"""
    new_category = Category(**data.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def update_category(db: Session, category_id: int, data: CategoryUpdate):
    """Cập nhật category"""
    category = get_category_by_id(db, category_id)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category_id: int):
    """Xóa category"""
    category = get_category_by_id(db, category_id)

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}
