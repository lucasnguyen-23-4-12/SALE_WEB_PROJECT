from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.address import AddressCreate
from app.services.exceptions import NotFoundException


def create_address(db: Session, data: AddressCreate):
    addr = Address(**data.model_dump())
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr


def get_addresses_by_customer(db: Session, customer_id: int):
    return db.query(Address).filter(Address.customer_id == customer_id).all()


def get_address_by_id(db: Session, address_id: int):
    address = db.query(Address).filter(Address.address_id == address_id).first()
    if not address:
        raise NotFoundException("Address")
    return address


def delete_address(db: Session, address_id: int):
    address = get_address_by_id(db, address_id)
    db.delete(address)
    db.commit()
    return {"message": "Address deleted"}