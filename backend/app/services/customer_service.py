from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.exceptions import *
from datetime import datetime
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_customer_by_id(db: Session, customer_id: int):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if not customer:
        raise NotFoundException("Customer")

    return customer


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


def update_customer(db: Session, customer_id: int, data: CustomerUpdate):

    customer = get_customer_by_id(db, customer_id)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(db: Session, customer_id: int):

    customer = get_customer_by_id(db, customer_id)

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}