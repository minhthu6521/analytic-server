"""add missing column

Revision ID: af6b6fd89778
Revises: 842925f4e56f
Create Date: 2018-11-11 13:53:45.357482

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'af6b6fd89778'
down_revision = '842925f4e56f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(u'user', sa.Column(u'language', sa.Integer()))
    op.add_column(u'position', sa.Column(u'internal_name', sa.String(255)))
    op.create_table('position_rights',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('position_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('json_data', mysql.MEDIUMTEXT(), nullable=True),
                    sa.Column('role', sa.String(length=64), nullable=True),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_foreign_key(u'position_right_position_fk', 'position_rights', 'position', ['position_id'], ['id'])
    op.create_foreign_key(u'position_right_user_fk1', 'position_rights', 'user', ['user_id'], ['id'])
    op.create_table('application_event',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('applicant_id', sa.Integer(), nullable=True),
                    sa.Column('application_event_token', sa.String(255)),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('status', sa.Integer()),
                    sa.Column('step', sa.String(255)),
                    sa.Column('time', sa.DateTime()),
                    sa.Column('note', sa.String(255)),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('duration', sa.Integer()))
    op.create_foreign_key(u'application_event_application_fk', 'application_event', 'application', ['applicant_id'], ['id'])
    op.create_foreign_key(u'application_event_user_fk', 'application_event', 'user', ['user_id'], ['id'])

    op.create_table('application_feedback',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('application_feedback_token', sa.String(255)),
                    sa.Column('application_id', sa.Integer(), nullable=True),
                    sa.Column('rating_time', sa.DateTime()),
                    sa.Column('rating_message', sa.Text()),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('rating', sa.Integer()))
    op.create_foreign_key(u'application_feedback_application_fk', 'application_feedback', 'application', ['application_id'],
                          ['id'])


def downgrade():
    op.drop_column(u'user', 'language')
    op.drop_column(u'position', 'internal_name')
    op.drop_table('position_rights')
