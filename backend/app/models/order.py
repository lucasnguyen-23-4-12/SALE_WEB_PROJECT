from sqlalchemy import Column, String, Date, ForeignKey, DECIMAL
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column("OrderID", String(50), primary_key=True, index=True, server_default=FetchedValue())
    customer_id = Column("CustomerID", String(50), ForeignKey("customers.CustomerID"), nullable=False)
    payment_method_id = Column("PaymentMethodID", String(50), ForeignKey("paymentmethods.PaymentMethodID"), nullable=False)
    order_date = Column("OrderDate", Date, nullable=False)
    status = Column("Status", String(50), nullable=False)
    shipping_address = Column("ShippingAddress", String(500))
    shipping_fee = Column("ShippingFee", DECIMAL(10,2), nullable=False, default=0.0)
    discount_amount = Column("DiscountAmount", DECIMAL(10,2), nullable=False, default=0.0)

    customer = relationship("Customer", back_populates="orders")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")
