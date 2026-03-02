from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column("OrderID", Integer, primary_key=True, index=True)
    customer_id = Column("CustomerID", Integer, ForeignKey("customers.CustomerID"))
    payment_method_id = Column("PaymentMethodID", Integer, ForeignKey("paymentmethods.PaymentMethodID"))
    order_date = Column("OrderDate", Date)
    status = Column("Status", String(50))

    customer = relationship("Customer", back_populates="orders")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")