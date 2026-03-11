"""Enforce NOT NULL on required order fields.

App schemas require customer_id, payment_method_id, order_date, status to be present.
This migration enforces the same at the DB level.

Revision ID: e9c1d2e3f4a5
Revises: d7f0a1b2c3d4
Create Date: 2026-03-11
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e9c1d2e3f4a5"
down_revision = "d7f0a1b2c3d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.text("UPDATE orders SET \"Status\" = 'Pending' WHERE \"Status\" IS NULL"))
    op.execute(sa.text("UPDATE orders SET \"OrderDate\" = CURRENT_DATE WHERE \"OrderDate\" IS NULL"))

    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
              IF EXISTS (SELECT 1 FROM orders WHERE "CustomerID" IS NULL) THEN
                RAISE EXCEPTION 'orders.CustomerID contains NULLs; cannot enforce NOT NULL';
              END IF;
              IF EXISTS (SELECT 1 FROM orders WHERE "PaymentMethodID" IS NULL) THEN
                RAISE EXCEPTION 'orders.PaymentMethodID contains NULLs; cannot enforce NOT NULL';
              END IF;
            END $$;
            """
        )
    )

    op.alter_column("orders", "CustomerID", existing_type=sa.Integer(), nullable=False)
    op.alter_column("orders", "PaymentMethodID", existing_type=sa.Integer(), nullable=False)
    op.alter_column("orders", "OrderDate", existing_type=sa.Date(), nullable=False)
    op.alter_column("orders", "Status", existing_type=sa.String(length=50), nullable=False)


def downgrade() -> None:
    op.alter_column("orders", "Status", existing_type=sa.String(length=50), nullable=True)
    op.alter_column("orders", "OrderDate", existing_type=sa.Date(), nullable=True)
    op.alter_column("orders", "PaymentMethodID", existing_type=sa.Integer(), nullable=True)
    op.alter_column("orders", "CustomerID", existing_type=sa.Integer(), nullable=True)

