from sqlalchemy import Column, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column("CategoryID", String(50), primary_key=True, index=True, server_default=FetchedValue())
    category_name = Column("CategoryName", String(255), nullable=False)
    subcategory = Column("Subcategory", String(255))

    products = relationship("Product", back_populates="category")
