from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class PaymentMethod(Base):
    __tablename__ = "paymentmethods"

    payment_method_id = Column("PaymentMethodID", Integer, primary_key=True, index=True)
    mode_name = Column("ModeName", String(100), nullable=False)
    pay_date = Column("PayDate", Date)

    orders = relationship("Order", back_populates="payment_method")