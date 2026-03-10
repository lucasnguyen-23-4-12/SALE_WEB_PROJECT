from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Wishlist(Base):
    __tablename__ = "wishlists"

    wishlist_id = Column("WishlistID", Integer, primary_key=True, index=True)
    customer_id = Column("CustomerID", Integer, ForeignKey("customers.CustomerID"), nullable=False)
    product_id = Column("ProductID", Integer, ForeignKey("products.ProductID"), nullable=False)

    customer = relationship("Customer", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlisted_by")
