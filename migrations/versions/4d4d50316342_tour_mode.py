"""Tour Mode

Revision ID: 4d4d50316342
Revises: 0efbc0665b32
Create Date: 2019-10-12 23:22:22.969509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d4d50316342'
down_revision = '0efbc0665b32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tour',
    sa.Column('tour_lock', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('tour_lock')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tour')
    # ### end Alembic commands ###
