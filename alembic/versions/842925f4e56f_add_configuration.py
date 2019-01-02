"""add configuration

Revision ID: 842925f4e56f
Revises: 710dce3e91c0
Create Date: 2018-11-11 12:21:04.513416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '842925f4e56f'
down_revision = '710dce3e91c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('configuration',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('last_fetch_date', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('configuration')
