"""Add FK and common-filter indexes for performance.

Revision ID: f1a2b3c4d5e6
Revises: e9c1d2e3f4a5
Create Date: 2026-03-11
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "f1a2b3c4d5e6"
down_revision = "e9c1d2e3f4a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Foreign key lookup/filter indexes
    op.create_index("ix_products_Category", "products", ["Category"], unique=False)

    op.create_index("ix_orders_CustomerID", "orders", ["CustomerID"], unique=False)
    op.create_index("ix_orders_PaymentMethodID", "orders", ["PaymentMethodID"], unique=False)
    op.create_index("ix_orders_OrderDate", "orders", ["OrderDate"], unique=False)

    op.create_index("ix_orderitems_OrderID", "orderitems", ["OrderID"], unique=False)
    op.create_index("ix_orderitems_ProductID", "orderitems", ["ProductID"], unique=False)

    op.create_index("ix_reviews_ProductID", "reviews", ["ProductID"], unique=False)
    op.create_index("ix_reviews_CustomerID", "reviews", ["CustomerID"], unique=False)

    op.create_index("ix_addresses_CustomerID", "addresses", ["CustomerID"], unique=False)

    op.create_index("ix_wishlists_CustomerID", "wishlists", ["CustomerID"], unique=False)
    op.create_index("ix_wishlists_ProductID", "wishlists", ["ProductID"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_wishlists_ProductID", table_name="wishlists")
    op.drop_index("ix_wishlists_CustomerID", table_name="wishlists")

    op.drop_index("ix_addresses_CustomerID", table_name="addresses")

    op.drop_index("ix_reviews_CustomerID", table_name="reviews")
    op.drop_index("ix_reviews_ProductID", table_name="reviews")

    op.drop_index("ix_orderitems_ProductID", table_name="orderitems")
    op.drop_index("ix_orderitems_OrderID", table_name="orderitems")

    op.drop_index("ix_orders_OrderDate", table_name="orders")
    op.drop_index("ix_orders_PaymentMethodID", table_name="orders")
    op.drop_index("ix_orders_CustomerID", table_name="orders")

    op.drop_index("ix_products_Category", table_name="products")

