from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from app.database import Base

class OrderItem(Base):
    __tablename__ = "orderitems"

    order_item_id = Column("OrderItemID", String(50), primary_key=True, index=True, server_default=FetchedValue())
    order_id = Column("OrderID", String(50), ForeignKey("orders.OrderID"), nullable=False)
    product_id = Column("ProductID", String(50), ForeignKey("products.ProductID"), nullable=False)
    quantity = Column("Quantity", Integer, nullable=False)
    amount = Column("Amount", DECIMAL(10,2))
    price_at_purchase = Column("PriceAtPurchase", DECIMAL(10,2))
    profit = Column("Profit", DECIMAL(10,2))
    discount = Column("Discount", DECIMAL(10,2))

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
