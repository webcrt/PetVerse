"""Added pet_id to VetAppointment

Revision ID: 404ff7c61e49
Revises: fadca9ebe37a
Create Date: 2026-02-17 14:19:24.240499
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '404ff7c61e49'
down_revision = 'fadca9ebe37a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('vet_appointment', schema=None) as batch_op:
        # Make it nullable because old records exist
        batch_op.add_column(sa.Column('pet_id', sa.Integer(), nullable=True))

        # Give the foreign key a NAME (required for SQLite)
        batch_op.create_foreign_key(
            'fk_vet_appointment_pet_id',
            'pet',
            ['pet_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('vet_appointment', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_vet_appointment_pet_id',
            type_='foreignkey'
        )
        batch_op.drop_column('pet_id')
