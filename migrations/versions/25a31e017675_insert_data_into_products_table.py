"""Insert data into products table

Revision ID: 25a31e017675
Revises: 2e0c94461a0d
Create Date: 2025-12-12 02:58:19.991787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25a31e017675'
down_revision = '2e0c94461a0d'
branch_labels = None
depends_on = None

def upgrade():
    categories_table = sa.table('categories',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String)
    )

    products_table = sa.table('products',
        sa.column('name', sa.String),
        sa.column('price', sa.Float),
        sa.column('active', sa.Boolean),
        sa.column('category_id', sa.Integer)
    )

    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'},
    ])


    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': 1},
        {'name': 'Smartphone', 'price': 800.0, 'active': True, 'category_id': 1},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': 2},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': 3},
    ])


def downgrade():
    op.execute("DELETE FROM products WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt')")
    op.execute("DELETE FROM categories WHERE name IN ('Electronics', 'Books', 'Clothing')")