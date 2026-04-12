"""expand retail schema

Revision ID: c3d4e5f6add
Revises: b74ea1262042
Create Date: 2026-03-04 10:15:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c3d4e5f6add'
down_revision = 'b74ea1262042'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add new columns to products
    op.add_column('products', sa.Column('DiscountPercent', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('products', sa.Column('StockQuantity', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('products', sa.Column('RatingAvg', sa.DECIMAL(precision=3, scale=2), nullable=False, server_default='0.0'))
    op.add_column('products', sa.Column('TotalReviews', sa.Integer(), nullable=False, server_default='0'))

    # customers modifications
    op.alter_column('customers', 'Creat_at', new_column_name='CreatedAt', existing_type=sa.Date())
    op.add_column('customers', sa.Column('UpdatedAt', sa.Date(), nullable=True))
    op.add_column('customers', sa.Column('IsActive', sa.Integer(), nullable=False, server_default='1'))

    # orders modifications
    op.add_column('orders', sa.Column('ShippingAddress', sa.String(length=500), nullable=True))
    op.add_column('orders', sa.Column('ShippingFee', sa.DECIMAL(10,2), nullable=False, server_default='0.0'))
    op.add_column('orders', sa.Column('DiscountAmount', sa.DECIMAL(10,2), nullable=False, server_default='0.0'))

    # create reviews table
    op.create_table('reviews',
        sa.Column('ReviewID', sa.Integer(), nullable=False),
        sa.Column('ProductID', sa.Integer(), nullable=False),
        sa.Column('CustomerID', sa.Integer(), nullable=False),
        sa.Column('Rating', sa.Integer(), nullable=False),
        sa.Column('Comment', sa.String(length=1000), nullable=True),
        sa.Column('CreatedAt', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['CustomerID'], ['customers.CustomerID'], ),
        sa.ForeignKeyConstraint(['ProductID'], ['products.ProductID'], ),
        sa.PrimaryKeyConstraint('ReviewID')
    )
    op.create_index(op.f('ix_reviews_ReviewID'), 'reviews', ['ReviewID'], unique=False)

    # create addresses table
    op.create_table('addresses',
        sa.Column('AddressID', sa.Integer(), nullable=False),
        sa.Column('CustomerID', sa.Integer(), nullable=False),
        sa.Column('Street', sa.String(length=500), nullable=True),
        sa.Column('City', sa.String(length=100), nullable=True),
        sa.Column('District', sa.String(length=100), nullable=True),
        sa.Column('Zipcode', sa.String(length=20), nullable=True),
        sa.Column('IsDefault', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['CustomerID'], ['customers.CustomerID'], ),
        sa.PrimaryKeyConstraint('AddressID')
    )
    op.create_index(op.f('ix_addresses_AddressID'), 'addresses', ['AddressID'], unique=False)

    # create wishlists table
    op.create_table('wishlists',
        sa.Column('WishlistID', sa.Integer(), nullable=False),
        sa.Column('CustomerID', sa.Integer(), nullable=False),
        sa.Column('ProductID', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['CustomerID'], ['customers.CustomerID'], ),
        sa.ForeignKeyConstraint(['ProductID'], ['products.ProductID'], ),
        sa.PrimaryKeyConstraint('WishlistID')
    )
    op.create_index(op.f('ix_wishlists_WishlistID'), 'wishlists', ['WishlistID'], unique=False)


def downgrade() -> None:
    # drop new tables
    op.drop_index(op.f('ix_wishlists_WishlistID'), table_name='wishlists')
    op.drop_table('wishlists')
    op.drop_index(op.f('ix_addresses_AddressID'), table_name='addresses')
    op.drop_table('addresses')
    op.drop_index(op.f('ix_reviews_ReviewID'), table_name='reviews')
    op.drop_table('reviews')

    # remove added columns from orders
    op.drop_column('orders', 'DiscountAmount')
    op.drop_column('orders', 'ShippingFee')
    op.drop_column('orders', 'ShippingAddress')

    # customers rollback
    op.drop_column('customers', 'IsActive')
    op.drop_column('customers', 'UpdatedAt')
    op.alter_column('customers', 'CreatedAt', new_column_name='Creat_at', existing_type=sa.Date())

    # products rollback
    op.drop_column('products', 'TotalReviews')
    op.drop_column('products', 'RatingAvg')
    op.drop_column('products', 'StockQuantity')
    op.drop_column('products', 'DiscountPercent')
