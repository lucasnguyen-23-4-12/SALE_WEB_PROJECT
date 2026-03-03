from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter()

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "DB injection working"}

from app.models.customer import Customer

@router.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers