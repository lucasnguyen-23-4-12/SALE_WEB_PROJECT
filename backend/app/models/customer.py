from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column("CustomerID", Integer, primary_key=True, index=True)
    customer_name = Column("CustomerName", String(255), nullable=False)
    customer_email = Column("CustomerEmail", String(255), unique=True, index=True, nullable=False)
    phone_number = Column("PhoneNumber", String(20))
    password_hash = Column("Password_Hash", String(255), nullable=False)
    address = Column("Address", String(500))
    created_at = Column("Creat_at", Date)

    orders = relationship("Order", back_populates="customer", cascade="all, delete")