from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class OrderItem(Base):
    __tablename__ = "orderitems"

    order_item_id = Column("OrderItemID", Integer, primary_key=True, index=True)
    order_id = Column("OrderID", Integer, ForeignKey("orders.OrderID"))
    product_id = Column("ProductID", Integer, ForeignKey("products.ProductID"))
    quantity = Column("Quantity", Integer, nullable=False)
    amount = Column("Amount", DECIMAL(10,2))
    price_at_purchase = Column("PriceAtPurchase", DECIMAL(10,2))
    profit = Column("Profit", DECIMAL(10,2))
    discount = Column("Discount", DECIMAL(10,2))

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")