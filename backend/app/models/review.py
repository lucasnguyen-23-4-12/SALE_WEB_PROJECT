from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column("ReviewID", Integer, primary_key=True, index=True)
    product_id = Column("ProductID", Integer, ForeignKey("products.ProductID"), nullable=False)
    customer_id = Column("CustomerID", Integer, ForeignKey("customers.CustomerID"), nullable=False)
    rating = Column("Rating", Integer, nullable=False)
    comment = Column("Comment", String(1000))
    created_at = Column("CreatedAt", DateTime)

    product = relationship("Product", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")
