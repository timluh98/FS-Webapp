"""fix purchase and order tables

Revision ID: ab6411d2083d
Revises: 
Create Date: 2024-12-14 15:04:31.465150
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ab6411d2083d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Drop existing tables if they exist
    op.execute('DROP TABLE IF EXISTS "order"')
    op.execute('DROP TABLE IF EXISTS purchase_new')
    
    # Create fresh order table
    op.create_table('order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('order_date', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('payment_status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('payment_reference', sa.String(100), nullable=True),
        sa.Column('payment_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create temporary table for purchase with auto-incrementing ID
    op.execute('''
        CREATE TABLE purchase_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            part_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price FLOAT NOT NULL,
            purchase_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(order_id) REFERENCES "order" (id),
            FOREIGN KEY(part_id) REFERENCES part (id),
            FOREIGN KEY(user_id) REFERENCES user (id)
        )
    ''')

    # Insert orders first, grouped by user and date
    op.execute('''
        INSERT INTO "order" (user_id, order_date, total_amount)
        SELECT 
            p.user_id,
            MIN(p.purchase_date),
            SUM(p.total_price)
        FROM purchase p
        GROUP BY p.user_id, date(p.purchase_date)
    ''')

    # Insert purchases with new IDs
    op.execute('''
        INSERT INTO purchase_new (part_id, user_id, quantity, total_price, purchase_date, order_id)
        SELECT 
            p.part_id,
            p.user_id,
            p.quantity,
            p.total_price,
            p.purchase_date,
            o.id
        FROM purchase p
        JOIN "order" o ON p.user_id = o.user_id 
        AND date(p.purchase_date) = date(o.order_date)
    ''')

    # Drop old purchase table and rename new one
    op.execute('DROP TABLE IF EXISTS purchase')
    op.execute('ALTER TABLE purchase_new RENAME TO purchase')

def downgrade():
    op.drop_table('purchase')
    op.drop_table('order')

