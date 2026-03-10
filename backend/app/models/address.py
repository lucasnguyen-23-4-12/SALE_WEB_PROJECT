from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Address(Base):
    __tablename__ = "addresses"

    address_id = Column("AddressID", Integer, primary_key=True, index=True)
    customer_id = Column("CustomerID", Integer, ForeignKey("customers.CustomerID"), nullable=False)
    street = Column("Street", String(500))
    city = Column("City", String(100))
    district = Column("District", String(100))
    zipcode = Column("Zipcode", String(20))
    is_default = Column("IsDefault", Integer, nullable=False, default=0)

    customer = relationship("Customer", back_populates="addresses")
