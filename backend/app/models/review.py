from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column("ReviewID", String(50), primary_key=True, index=True, server_default=FetchedValue())
    product_id = Column("ProductID", String(50), ForeignKey("products.ProductID"), nullable=False)
    customer_id = Column("CustomerID", String(50), ForeignKey("customers.CustomerID"), nullable=False)
    rating = Column("Rating", Integer, nullable=False)
    comment = Column("Comment", String(1000))
    created_at = Column("CreatedAt", DateTime)

    product = relationship("Product", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")
