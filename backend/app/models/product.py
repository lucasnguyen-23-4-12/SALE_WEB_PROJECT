from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column("ProductID", Integer, primary_key=True, index=True)
    category_id = Column("Category", Integer, ForeignKey("categories.CategoryID"))
    product_name = Column("ProductName", String(255), nullable=False)
    description = Column("Description", String(1000))
    image_url = Column("Image_url", String(500))
    unit_price = Column("UnitPrice", DECIMAL(10,2), nullable=False)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")