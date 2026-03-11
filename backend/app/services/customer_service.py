from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.exceptions import *
from datetime import datetime
import hashlib
from passlib.context import CryptContext


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    if stored_hash.startswith("$2"):
        return _pwd_context.verify(password, stored_hash)
    return stored_hash == _sha256(password)


def get_customer_by_id(db: Session, customer_id: str):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if not customer:
        raise NotFoundException("Customer")

    return customer


def get_all_customers(db: Session, skip: int = 0, limit: int = 10):
    """Lấy tất cả customers (có pagination)"""
    return db.query(Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, data: CustomerCreate):

    existing = db.query(Customer).filter(
        Customer.customer_email == data.customer_email
    ).first()

    if existing:
        raise AlreadyExistsException("Email")

    new_customer = Customer(
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        phone_number=data.phone_number,
        address=data.address,
        password_hash=hash_password(data.password),
        created_at=datetime.utcnow()
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def authenticate_customer(db: Session, email_or_phone: str, password: str):
    """Xác thực customer bằng email/phone và password"""
    customer = db.query(Customer).filter(
        (Customer.customer_email == email_or_phone) |
        (Customer.phone_number == email_or_phone)
    ).first()

    if not customer:
        raise NotFoundException("Customer")

    if not verify_password(password, customer.password_hash):
        raise ValidationException("Invalid password")

    if not customer.password_hash.startswith("$2"):
        customer.password_hash = hash_password(password)
        db.commit()
        db.refresh(customer)

    return customer


def update_customer(db: Session, customer_id: str, data: CustomerUpdate):

    customer = get_customer_by_id(db, customer_id)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(db: Session, customer_id: str):

    customer = get_customer_by_id(db, customer_id)

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}
