"""Add sites

Revision ID: d5cb0d93b970
Revises: 0cc3557c43d0
Create Date: 2017-05-09 11:37:47.244859

"""
from alembic import op
import sqlalchemy as sa
import model.utils


from participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus
from participant_enums import WithdrawalStatus, SuspensionStatus
from participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType
from model.code import CodeType

# revision identifiers, used by Alembic.
revision = 'd5cb0d93b970'
down_revision = '0cc3557c43d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site',
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('site_name', sa.String(length=255), nullable=False),
    sa.Column('google_group', sa.String(length=255), nullable=False),
    sa.Column('consortium_name', sa.String(length=255), nullable=False),
    sa.Column('mayolink_client_number', sa.Integer(), nullable=True),
    sa.Column('hpo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hpo_id'], ['hpo.hpo_id'], ),
    sa.PrimaryKeyConstraint('site_id'),
    sa.UniqueConstraint('google_group')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('site')
    # ### end Alembic commands ###
