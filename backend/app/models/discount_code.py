from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class DiscountCode(Base):
    __tablename__ = "discountcodes"

    discount_code_id = Column("DiscountCodeID", String(50), primary_key=True, index=True)
    code = Column("Code", String(50), nullable=False, unique=True, index=True)
    description = Column("Description", String(500))
    discount_percent = Column("DiscountPercent", Integer, nullable=False, default=0)
    product_id = Column(
        "ProductID",
        String(50),
        ForeignKey("products.ProductID", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    customer_id = Column(
        "CustomerID",
        String(50),
        ForeignKey("customers.CustomerID", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    usage_limit = Column("UsageLimit", Integer, nullable=False, default=1)
    used_count = Column("UsedCount", Integer, nullable=False, default=0)
    starts_at = Column("StartsAt", DateTime, nullable=True)
    expires_at = Column("ExpiresAt", DateTime, nullable=True)
    is_active = Column("IsActive", Boolean, nullable=False, default=True)
    created_at = Column("CreatedAt", DateTime, nullable=False, default=datetime.utcnow)

    product = relationship("Product", back_populates="discount_codes")
    customer = relationship("Customer", back_populates="discount_codes")
