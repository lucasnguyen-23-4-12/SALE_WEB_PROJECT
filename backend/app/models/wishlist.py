from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from app.database import Base

class Wishlist(Base):
    __tablename__ = "wishlists"

    wishlist_id = Column("WishlistID", String(50), primary_key=True, index=True, server_default=FetchedValue())
    customer_id = Column("CustomerID", String(50), ForeignKey("customers.CustomerID"), nullable=False)
    product_id = Column("ProductID", String(50), ForeignKey("products.ProductID"), nullable=False)

    customer = relationship("Customer", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlisted_by")
