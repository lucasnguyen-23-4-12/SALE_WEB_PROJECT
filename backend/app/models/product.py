from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column("ProductID", String(50), primary_key=True, index=True, server_default=FetchedValue())
    category_id = Column("Category", String(50), ForeignKey("categories.CategoryID"), nullable=False)
    product_name = Column("ProductName", String(255), nullable=False)
    description = Column("Description", String(1000))
    image_url = Column("Image_url", String(500))
    unit_price = Column("UnitPrice", DECIMAL(10,2), nullable=False)
    discount_percent = Column("DiscountPercent", Integer, nullable=False, default=0)
    stock_quantity = Column("StockQuantity", Integer, nullable=False, default=0)
    rating_avg = Column("RatingAvg", DECIMAL(3,2), nullable=False, default=0.0)
    total_reviews = Column("TotalReviews", Integer, nullable=False, default=0)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    reviews = relationship("Review", back_populates="product", cascade="all, delete")
    wishlisted_by = relationship("Wishlist", back_populates="product", cascade="all, delete")
    discount_codes = relationship("DiscountCode", back_populates="product")
