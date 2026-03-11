from sqlalchemy.orm import Session
from app.models.payment_method import PaymentMethod
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate
from app.services.exceptions import *


def get_payment_method_by_id(db: Session, payment_method_id: str):
    """Lấy payment method theo ID"""
    payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.payment_method_id == payment_method_id
    ).first()

    if not payment_method:
        raise NotFoundException("Payment method")

    return payment_method


def get_all_payment_methods(db: Session, skip: int = 0, limit: int = 10):
    """Lấy tất cả payment methods (có pagination)"""
    return db.query(PaymentMethod).offset(skip).limit(limit).all()


def create_payment_method(db: Session, data: PaymentMethodCreate):
    """Tạo payment method mới"""
    new_payment_method = PaymentMethod(**data.model_dump())

    db.add(new_payment_method)
    db.commit()
    db.refresh(new_payment_method)

    return new_payment_method


def update_payment_method(db: Session, payment_method_id: str, data: PaymentMethodUpdate):
    """Cập nhật payment method"""
    payment_method = get_payment_method_by_id(db, payment_method_id)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(payment_method, field, value)

    db.commit()
    db.refresh(payment_method)

    return payment_method


def delete_payment_method(db: Session, payment_method_id: str):
    """Xóa payment method"""
    payment_method = get_payment_method_by_id(db, payment_method_id)

    db.delete(payment_method)
    db.commit()

    return {"message": "Payment method deleted successfully"}
