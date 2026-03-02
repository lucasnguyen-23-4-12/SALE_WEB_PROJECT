from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column("CategoryID", Integer, primary_key=True, index=True)
    category_name = Column("CategoryName", String(255), nullable=False)
    subcategory = Column("Subcategory", String(255))

    products = relationship("Product", back_populates="category")