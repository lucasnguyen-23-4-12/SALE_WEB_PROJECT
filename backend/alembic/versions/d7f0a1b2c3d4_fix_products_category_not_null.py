"""Fix products.Category NULLs and enforce NOT NULL.

Revision ID: d7f0a1b2c3d4
Revises: c3d4e5f6add
Create Date: 2026-03-11
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d7f0a1b2c3d4"
down_revision = "c3d4e5f6add"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            DO $$
            DECLARE default_category_id integer;
            BEGIN
              SELECT "CategoryID"
                INTO default_category_id
                FROM categories
                ORDER BY "CategoryID"
                LIMIT 1;

              IF default_category_id IS NULL THEN
                INSERT INTO categories ("CategoryName", "Subcategory")
                VALUES ('Uncategorized', NULL)
                RETURNING "CategoryID" INTO default_category_id;
              END IF;

              UPDATE products
                 SET "Category" = default_category_id
               WHERE "Category" IS NULL;
            END $$;
            """
        )
    )

    op.alter_column(
        "products",
        "Category",
        existing_type=sa.Integer(),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "products",
        "Category",
        existing_type=sa.Integer(),
        nullable=True,
    )
