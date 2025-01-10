"""initial database setup

Revision ID: initial_setup_v1
Revises: 
Create Date: 2024-12-14 21:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = 'initial_setup_v1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create user table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(150), nullable=False),
        sa.Column('email', sa.String(150), nullable=False),
        sa.Column('password', sa.String(200), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create part table
    op.create_table('part',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('availability', sa.String(100), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('delivery', sa.String(100), nullable=False),
        sa.Column('image', sa.String(200), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('manufacturer', sa.String(100), nullable=False),
        sa.Column('model', sa.String(100), nullable=False),
        sa.ForeignKeyConstraint(['supplier_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create order table
    op.create_table('order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('order_date', sa.DateTime(), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('payment_status', sa.String(20), nullable=False),
        sa.Column('payment_reference', sa.String(100), nullable=True),
        sa.Column('payment_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create purchase table with all fields including delivery info
    op.create_table('purchase',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('part_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('purchase_date', sa.DateTime(), nullable=False),
        sa.Column('delivery_name', sa.String(150), nullable=False),
        sa.Column('delivery_street', sa.String(200), nullable=False),
        sa.Column('delivery_city', sa.String(100), nullable=False),
        sa.Column('delivery_postal_code', sa.String(20), nullable=False),
        sa.Column('delivery_country', sa.String(100), nullable=False),
        sa.Column('delivery_phone', sa.String(50), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
        sa.ForeignKeyConstraint(['part_id'], ['part.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('purchase')
    op.drop_table('order')
    op.drop_table('part')
    op.drop_table('user')
