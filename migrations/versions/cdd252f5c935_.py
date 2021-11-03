"""empty message

Revision ID: cdd252f5c935
Revises: a3da8cc6d6da
Create Date: 2021-10-08 15:35:59.126189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdd252f5c935'
down_revision = 'a3da8cc6d6da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hits', sa.Integer(), server_default='0', nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.drop_column('hits')

    # ### end Alembic commands ###