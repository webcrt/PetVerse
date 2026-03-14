"""Add status column to OrderItem safely

Revision ID: 4d917dd5280c
Revises: 9b3b2d525826
Create Date: 2025-09-20 13:12:18.091950
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4d917dd5280c'
down_revision = '9b3b2d525826'
branch_labels = None
depends_on = None


def upgrade():
    # Ensure existing rows comply with NOT NULL constraint
    op.execute("""
        UPDATE order_item
        SET supplier_id = 1
        WHERE supplier_id IS NULL
    """)

    # Safely alter the table
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        # Add 'status' column with default
        batch_op.add_column(
            sa.Column(
                'status',
                sa.String(length=20),
                nullable=False,
                server_default='pending'
            )
        )
        # Enforce NOT NULL on supplier_id
        batch_op.alter_column(
            'supplier_id',
            existing_type=sa.INTEGER(),
            nullable=False
        )


def downgrade():
    # Revert changes
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.drop_column('status')
        batch_op.alter_column(
            'supplier_id',
            existing_type=sa.INTEGER(),
            nullable=True
        )
