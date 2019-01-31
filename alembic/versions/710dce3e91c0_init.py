"""init

Revision ID: 710dce3e91c0
Revises: 
Create Date: 2018-11-03 16:10:18.394090

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '710dce3e91c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('company',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('company_token', sa.String(length=255), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('business_unit',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('name', sa.String(255), nullable=True),
                    sa.Column('business_unit_token', sa.String(length=255), nullable=False),
                    sa.Column('parent_id', sa.Integer()),
                    sa.Column('company_id', sa.Integer(), nullable=False),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('json_data', sa.Text(), nullable=True)
                    )
    op.create_foreign_key(u'business_unit_ibfk_1', 'business_unit', 'company', ['company_id'], ['id'])
    op.create_foreign_key(u'business_unit_parent_fk', 'business_unit', 'business_unit', ['parent_id'], ['id'])
    op.create_table('user',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('user_token', sa.String(length=255), nullable=False),
                    sa.Column('first_name', sa.String(length=255), nullable=True),
                    sa.Column('last_name', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('title', sa.String(length=255), nullable=True),
                    sa.Column('password', sa.String(length=255), nullable=True),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
                    sa.Column('last_login_at', sa.DateTime(), nullable=True),
                    sa.Column('current_login_at', sa.DateTime(), nullable=True),
                    sa.Column('login_count', sa.Integer(), nullable=True),
                    sa.Column('photoname', sa.String(length=255), nullable=True),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('roles', sa.Text(), nullable=True)
                    )
    op.create_foreign_key(u'company_userfk_1', 'user', 'company', ['company_id'], ['id'])
    op.create_table('position',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('position_token', sa.String(length=255), nullable=False),
                    sa.Column('language', sa.Integer(), nullable=True),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('expiration_date', sa.DateTime(), nullable=True),
                    sa.Column('starting_date', sa.DateTime(), nullable=True),
                    sa.Column('approval_time', sa.DateTime(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('template_id', sa.String(length=255), nullable=True),
                    sa.Column('link', sa.String(length=255), nullable=True),
                    sa.Column('status', sa.Integer(), nullable=True),
                    sa.Column('business_unit_id', sa.Integer()),
                    sa.Column('employment_type', sa.String(length=255), nullable=True),
                    sa.Column('reason_for_vacancy', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_foreign_key(u'position_ibfk_1', 'position', 'company', ['company_id'], ['id'])
    op.create_foreign_key(u'job_business_unit_fk', 'position', 'business_unit', ['business_unit_id'], ['id'])
    op.create_table('ad_view_counters',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('position_id', sa.Integer(), nullable=True),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('time', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('talent',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('talent_token', sa.String(length=255), nullable=False),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('time_confirmed_membership', sa.DateTime(), nullable=True),
                    sa.Column('time_added_to_talent_community', sa.DateTime(), nullable=True),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.Column('talent_community', sa.Boolean(), server_default='0'),
                    sa.Column('confirmed_talent_community', sa.Boolean(), server_default='0'),
                    sa.Column('language', sa.Integer(), nullable=True),
                    sa.Column('image', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_foreign_key(u'company_talent_fk', 'talent', 'company', ['company_id'], ['id'])
    op.create_table('community',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_foreign_key(u'community_ibfk_1', 'community', 'company', ['company_id'], ['id'], ondelete='CASCADE')
    op.create_table('talent_communities',
                    sa.Column('talent_id', sa.Integer(), nullable=False),
                    sa.Column('community_id', sa.Integer(), nullable=False),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('talent_id', 'community_id')
                    )
    op.create_foreign_key(u'talent_communities_talent_fk', 'talent_communities', 'talent', ['talent_id'], ['id'],
                          ondelete='CASCADE')
    op.create_foreign_key(u'talent_communities_community_fk', 'talent_communities', 'community', ['community_id'], ['id'],
                          ondelete='CASCADE')
    op.create_table('application',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('application_token', sa.String(length=255), nullable=False),
                    sa.Column('time_created', sa.DateTime(), nullable=True),
                    sa.Column('time_modified', sa.DateTime(), nullable=True),
                    sa.Column('position_id', sa.Integer(), nullable=True),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.Column('talent_id', sa.Integer(), nullable=True),
                    sa.Column('status', sa.Integer(), nullable=True),
                    sa.Column('language', sa.Integer(), nullable=True),
                    sa.Column('image', sa.String(length=255), nullable=True),
                    sa.Column('application_date', sa.DateTime(), nullable=True),
                    sa.Column('step', sa.String(length=255), nullable=True),
                    sa.Column('outcome_status',sa.Integer(), nullable=True),
                    sa.Column('outcome_email_status', sa.String(255)),
                    sa.Column('want_feedback',sa.Boolean(), default=True, server_default='1'),
                    sa.Column('average_rating', sa.Float(), nullable=True),
                    sa.Column('feedback_score', sa.Float(), default=None),
                    sa.Column('feedback_rating', sa.Float(), default=None),
                    sa.Column('recommendation_similarity', sa.Float(), default=None),
                    sa.Column('json_ratings', mysql.MEDIUMTEXT(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_foreign_key(u'application_position_fk', 'application', 'position', ['position_id'], ['id'])
    op.create_foreign_key(u'application_company_fk', 'application', 'company', ['company_id'], ['id'])
    op.create_foreign_key(u'application_talent_fk', 'application', 'talent', ['talent_id'], ['id'])
    op.create_table('interview_slot',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('begins', sa.DateTime(), nullable=False),
                    sa.Column('ends', sa.DateTime(), nullable=False),
                    sa.Column('for_applicant_status', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offered_slot',
                    sa.Column('slot_id', sa.Integer(), nullable=False),
                    sa.Column('application_id', sa.Integer(), nullable=False),
                    sa.Column('confirmation', sa.String(length=64), nullable=True),
                    sa.ForeignKeyConstraint(['application_id'], ['application.id'], ),
                    sa.ForeignKeyConstraint(['slot_id'], ['interview_slot.id'], ),
                    sa.PrimaryKeyConstraint('slot_id', 'application_id')
    )


def downgrade():
    op.drop_table('offered_slot')
    op.drop_table('interview_slot')
    op.drop_table('application')
    op.drop_table('talent_communities')
    op.drop_table('community')
    op.drop_table('talent')
    op.drop_table('ad_view_counters')
    op.drop_table('position')
    op.drop_table('user')
    op.drop_table('business_unit')
    op.drop_table('company')
