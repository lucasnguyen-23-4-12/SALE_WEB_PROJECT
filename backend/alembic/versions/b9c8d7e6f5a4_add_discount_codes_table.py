"""add discount codes table for admin management

Revision ID: b9c8d7e6f5a4
Revises: a1b2c3d4e5f6
Create Date: 2026-04-08 19:10:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "b9c8d7e6f5a4"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "discountcodes",
        sa.Column("DiscountCodeID", sa.String(length=50), nullable=False),
        sa.Column("Code", sa.String(length=50), nullable=False),
        sa.Column("Description", sa.String(length=500), nullable=True),
        sa.Column("DiscountPercent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ProductID", sa.String(length=50), nullable=True),
        sa.Column("CustomerID", sa.String(length=50), nullable=True),
        sa.Column("UsageLimit", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("UsedCount", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("StartsAt", sa.DateTime(), nullable=True),
        sa.Column("ExpiresAt", sa.DateTime(), nullable=True),
        sa.Column("IsActive", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("CreatedAt", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["CustomerID"], ["customers.CustomerID"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["ProductID"], ["products.ProductID"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("DiscountCodeID"),
        sa.UniqueConstraint("Code"),
    )
    op.create_index("ix_discountcodes_DiscountCodeID", "discountcodes", ["DiscountCodeID"], unique=False)
    op.create_index("ix_discountcodes_Code", "discountcodes", ["Code"], unique=True)
    op.create_index("ix_discountcodes_ProductID", "discountcodes", ["ProductID"], unique=False)
    op.create_index("ix_discountcodes_CustomerID", "discountcodes", ["CustomerID"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_discountcodes_CustomerID", table_name="discountcodes")
    op.drop_index("ix_discountcodes_ProductID", table_name="discountcodes")
    op.drop_index("ix_discountcodes_Code", table_name="discountcodes")
    op.drop_index("ix_discountcodes_DiscountCodeID", table_name="discountcodes")
    op.drop_table("discountcodes")
