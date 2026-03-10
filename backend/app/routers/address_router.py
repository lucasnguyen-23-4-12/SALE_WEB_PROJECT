from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.address import AddressCreate, AddressResponse
from app.services import address_service
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)

@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(payload: AddressCreate, db: Session = Depends(get_db)):
    return address_service.create_address(db, payload)

@router.get("/customer/{customer_id}", response_model=List[AddressResponse])
def get_addresses(customer_id: int, db: Session = Depends(get_db)):
    return address_service.get_addresses_by_customer(db, customer_id)

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_service.delete_address(db, address_id)