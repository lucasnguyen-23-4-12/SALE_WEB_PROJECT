"""Convert all PK/FK IDs from INT to VARCHAR and tighten constraints.

This keeps existing numeric IDs but stores them as strings (varchar),
using the existing sequences as defaults (nextval(...)::text).

Revision ID: a1b2c3d4e5f6
Revises: f1a2b3c4d5e6
Create Date: 2026-03-11
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop FKs first
    op.execute(sa.text('ALTER TABLE addresses DROP CONSTRAINT IF EXISTS "addresses_CustomerID_fkey"'))
    op.execute(sa.text('ALTER TABLE orderitems DROP CONSTRAINT IF EXISTS "orderitems_OrderID_fkey"'))
    op.execute(sa.text('ALTER TABLE orderitems DROP CONSTRAINT IF EXISTS "orderitems_ProductID_fkey"'))
    op.execute(sa.text('ALTER TABLE orders DROP CONSTRAINT IF EXISTS "orders_CustomerID_fkey"'))
    op.execute(sa.text('ALTER TABLE orders DROP CONSTRAINT IF EXISTS "orders_PaymentMethodID_fkey"'))
    op.execute(sa.text('ALTER TABLE products DROP CONSTRAINT IF EXISTS "products_Category_fkey"'))
    op.execute(sa.text('ALTER TABLE reviews DROP CONSTRAINT IF EXISTS "reviews_CustomerID_fkey"'))
    op.execute(sa.text('ALTER TABLE reviews DROP CONSTRAINT IF EXISTS "reviews_ProductID_fkey"'))
    op.execute(sa.text('ALTER TABLE wishlists DROP CONSTRAINT IF EXISTS "wishlists_CustomerID_fkey"'))
    op.execute(sa.text('ALTER TABLE wishlists DROP CONSTRAINT IF EXISTS "wishlists_ProductID_fkey"'))

    # Drop indexes that depend on ID/FK column types (keep email index)
    for idx in [
        "ix_addresses_AddressID",
        "ix_categories_CategoryID",
        "ix_customers_CustomerID",
        "ix_orderitems_OrderItemID",
        "ix_orders_OrderID",
        "ix_paymentmethods_PaymentMethodID",
        "ix_products_ProductID",
        "ix_reviews_ReviewID",
        "ix_wishlists_WishlistID",
        # Phase 13 indexes
        "ix_products_Category",
        "ix_orders_CustomerID",
        "ix_orders_PaymentMethodID",
        "ix_orders_OrderDate",
        "ix_orderitems_OrderID",
        "ix_orderitems_ProductID",
        "ix_reviews_ProductID",
        "ix_reviews_CustomerID",
        "ix_addresses_CustomerID",
        "ix_wishlists_CustomerID",
        "ix_wishlists_ProductID",
    ]:
        op.execute(sa.text(f'DROP INDEX IF EXISTS "{idx}"'))

    # Drop PK constraints (they will be recreated)
    for t in [
        "addresses",
        "categories",
        "customers",
        "orderitems",
        "orders",
        "paymentmethods",
        "products",
        "reviews",
        "wishlists",
    ]:
        op.execute(sa.text(f'ALTER TABLE {t} DROP CONSTRAINT IF EXISTS "{t}_pkey"'))

    # Convert PKs to VARCHAR and keep sequence defaults
    op.execute(sa.text('ALTER TABLE categories ALTER COLUMN "CategoryID" TYPE VARCHAR(50) USING "CategoryID"::text'))
    op.execute(sa.text('ALTER TABLE categories ALTER COLUMN "CategoryID" SET DEFAULT nextval(\'"categories_CategoryID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE customers ALTER COLUMN "CustomerID" TYPE VARCHAR(50) USING "CustomerID"::text'))
    op.execute(sa.text('ALTER TABLE customers ALTER COLUMN "CustomerID" SET DEFAULT nextval(\'"customers_CustomerID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE paymentmethods ALTER COLUMN "PaymentMethodID" TYPE VARCHAR(50) USING "PaymentMethodID"::text'))
    op.execute(sa.text('ALTER TABLE paymentmethods ALTER COLUMN "PaymentMethodID" SET DEFAULT nextval(\'"paymentmethods_PaymentMethodID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE products ALTER COLUMN "ProductID" TYPE VARCHAR(50) USING "ProductID"::text'))
    op.execute(sa.text('ALTER TABLE products ALTER COLUMN "ProductID" SET DEFAULT nextval(\'"products_ProductID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE orders ALTER COLUMN "OrderID" TYPE VARCHAR(50) USING "OrderID"::text'))
    op.execute(sa.text('ALTER TABLE orders ALTER COLUMN "OrderID" SET DEFAULT nextval(\'"orders_OrderID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE orderitems ALTER COLUMN "OrderItemID" TYPE VARCHAR(50) USING "OrderItemID"::text'))
    op.execute(sa.text('ALTER TABLE orderitems ALTER COLUMN "OrderItemID" SET DEFAULT nextval(\'"orderitems_OrderItemID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE reviews ALTER COLUMN "ReviewID" TYPE VARCHAR(50) USING "ReviewID"::text'))
    op.execute(sa.text('ALTER TABLE reviews ALTER COLUMN "ReviewID" SET DEFAULT nextval(\'"reviews_ReviewID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE addresses ALTER COLUMN "AddressID" TYPE VARCHAR(50) USING "AddressID"::text'))
    op.execute(sa.text('ALTER TABLE addresses ALTER COLUMN "AddressID" SET DEFAULT nextval(\'"addresses_AddressID_seq"\'::regclass)::text'))

    op.execute(sa.text('ALTER TABLE wishlists ALTER COLUMN "WishlistID" TYPE VARCHAR(50) USING "WishlistID"::text'))
    op.execute(sa.text('ALTER TABLE wishlists ALTER COLUMN "WishlistID" SET DEFAULT nextval(\'"wishlists_WishlistID_seq"\'::regclass)::text'))

    # Convert FK columns to VARCHAR
    op.execute(sa.text('ALTER TABLE products ALTER COLUMN "Category" TYPE VARCHAR(50) USING "Category"::text'))

    op.execute(sa.text('ALTER TABLE orders ALTER COLUMN "CustomerID" TYPE VARCHAR(50) USING "CustomerID"::text'))
    op.execute(sa.text('ALTER TABLE orders ALTER COLUMN "PaymentMethodID" TYPE VARCHAR(50) USING "PaymentMethodID"::text'))

    op.execute(sa.text('ALTER TABLE orderitems ALTER COLUMN "OrderID" TYPE VARCHAR(50) USING "OrderID"::text'))
    op.execute(sa.text('ALTER TABLE orderitems ALTER COLUMN "ProductID" TYPE VARCHAR(50) USING "ProductID"::text'))

    op.execute(sa.text('ALTER TABLE reviews ALTER COLUMN "ProductID" TYPE VARCHAR(50) USING "ProductID"::text'))
    op.execute(sa.text('ALTER TABLE reviews ALTER COLUMN "CustomerID" TYPE VARCHAR(50) USING "CustomerID"::text'))

    op.execute(sa.text('ALTER TABLE addresses ALTER COLUMN "CustomerID" TYPE VARCHAR(50) USING "CustomerID"::text'))

    op.execute(sa.text('ALTER TABLE wishlists ALTER COLUMN "CustomerID" TYPE VARCHAR(50) USING "CustomerID"::text'))
    op.execute(sa.text('ALTER TABLE wishlists ALTER COLUMN "ProductID" TYPE VARCHAR(50) USING "ProductID"::text'))

    # Tighten constraints: orderitems FK columns must not be NULL.
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
              IF EXISTS (SELECT 1 FROM orderitems WHERE "OrderID" IS NULL OR "ProductID" IS NULL) THEN
                RAISE EXCEPTION 'orderitems contains NULL FK values; cannot enforce NOT NULL';
              END IF;
            END $$;
            """
        )
    )
    op.execute(sa.text('ALTER TABLE orderitems ALTER COLUMN "OrderID" SET NOT NULL'))
    op.execute(sa.text('ALTER TABLE orderitems ALTER COLUMN "ProductID" SET NOT NULL'))

    # Recreate PK constraints
    op.execute(sa.text('ALTER TABLE categories ADD CONSTRAINT "categories_pkey" PRIMARY KEY ("CategoryID")'))
    op.execute(sa.text('ALTER TABLE customers ADD CONSTRAINT "customers_pkey" PRIMARY KEY ("CustomerID")'))
    op.execute(sa.text('ALTER TABLE paymentmethods ADD CONSTRAINT "paymentmethods_pkey" PRIMARY KEY ("PaymentMethodID")'))
    op.execute(sa.text('ALTER TABLE products ADD CONSTRAINT "products_pkey" PRIMARY KEY ("ProductID")'))
    op.execute(sa.text('ALTER TABLE orders ADD CONSTRAINT "orders_pkey" PRIMARY KEY ("OrderID")'))
    op.execute(sa.text('ALTER TABLE orderitems ADD CONSTRAINT "orderitems_pkey" PRIMARY KEY ("OrderItemID")'))
    op.execute(sa.text('ALTER TABLE reviews ADD CONSTRAINT "reviews_pkey" PRIMARY KEY ("ReviewID")'))
    op.execute(sa.text('ALTER TABLE addresses ADD CONSTRAINT "addresses_pkey" PRIMARY KEY ("AddressID")'))
    op.execute(sa.text('ALTER TABLE wishlists ADD CONSTRAINT "wishlists_pkey" PRIMARY KEY ("WishlistID")'))

    # Recreate FKs
    op.execute(
        sa.text(
            'ALTER TABLE products ADD CONSTRAINT "products_Category_fkey" FOREIGN KEY ("Category") REFERENCES categories("CategoryID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE orders ADD CONSTRAINT "orders_CustomerID_fkey" FOREIGN KEY ("CustomerID") REFERENCES customers("CustomerID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE orders ADD CONSTRAINT "orders_PaymentMethodID_fkey" FOREIGN KEY ("PaymentMethodID") REFERENCES paymentmethods("PaymentMethodID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE orderitems ADD CONSTRAINT "orderitems_OrderID_fkey" FOREIGN KEY ("OrderID") REFERENCES orders("OrderID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE orderitems ADD CONSTRAINT "orderitems_ProductID_fkey" FOREIGN KEY ("ProductID") REFERENCES products("ProductID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE reviews ADD CONSTRAINT "reviews_ProductID_fkey" FOREIGN KEY ("ProductID") REFERENCES products("ProductID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE reviews ADD CONSTRAINT "reviews_CustomerID_fkey" FOREIGN KEY ("CustomerID") REFERENCES customers("CustomerID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE addresses ADD CONSTRAINT "addresses_CustomerID_fkey" FOREIGN KEY ("CustomerID") REFERENCES customers("CustomerID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE wishlists ADD CONSTRAINT "wishlists_CustomerID_fkey" FOREIGN KEY ("CustomerID") REFERENCES customers("CustomerID")'
        )
    )
    op.execute(
        sa.text(
            'ALTER TABLE wishlists ADD CONSTRAINT "wishlists_ProductID_fkey" FOREIGN KEY ("ProductID") REFERENCES products("ProductID")'
        )
    )

    # Recreate indexes (including Phase 13 indexes)
    op.execute(sa.text('CREATE INDEX "ix_categories_CategoryID" ON categories ("CategoryID")'))
    op.execute(sa.text('CREATE INDEX "ix_customers_CustomerID" ON customers ("CustomerID")'))
    op.execute(sa.text('CREATE INDEX "ix_paymentmethods_PaymentMethodID" ON paymentmethods ("PaymentMethodID")'))
    op.execute(sa.text('CREATE INDEX "ix_products_ProductID" ON products ("ProductID")'))
    op.execute(sa.text('CREATE INDEX "ix_orders_OrderID" ON orders ("OrderID")'))
    op.execute(sa.text('CREATE INDEX "ix_orderitems_OrderItemID" ON orderitems ("OrderItemID")'))
    op.execute(sa.text('CREATE INDEX "ix_reviews_ReviewID" ON reviews ("ReviewID")'))
    op.execute(sa.text('CREATE INDEX "ix_addresses_AddressID" ON addresses ("AddressID")'))
    op.execute(sa.text('CREATE INDEX "ix_wishlists_WishlistID" ON wishlists ("WishlistID")'))

    op.execute(sa.text('CREATE INDEX "ix_products_Category" ON products ("Category")'))
    op.execute(sa.text('CREATE INDEX "ix_orders_CustomerID" ON orders ("CustomerID")'))
    op.execute(sa.text('CREATE INDEX "ix_orders_PaymentMethodID" ON orders ("PaymentMethodID")'))
    op.execute(sa.text('CREATE INDEX "ix_orders_OrderDate" ON orders ("OrderDate")'))
    op.execute(sa.text('CREATE INDEX "ix_orderitems_OrderID" ON orderitems ("OrderID")'))
    op.execute(sa.text('CREATE INDEX "ix_orderitems_ProductID" ON orderitems ("ProductID")'))
    op.execute(sa.text('CREATE INDEX "ix_reviews_ProductID" ON reviews ("ProductID")'))
    op.execute(sa.text('CREATE INDEX "ix_reviews_CustomerID" ON reviews ("CustomerID")'))
    op.execute(sa.text('CREATE INDEX "ix_addresses_CustomerID" ON addresses ("CustomerID")'))
    op.execute(sa.text('CREATE INDEX "ix_wishlists_CustomerID" ON wishlists ("CustomerID")'))
    op.execute(sa.text('CREATE INDEX "ix_wishlists_ProductID" ON wishlists ("ProductID")'))


def downgrade() -> None:
    raise RuntimeError("Downgrade not supported for ID type conversion.")

