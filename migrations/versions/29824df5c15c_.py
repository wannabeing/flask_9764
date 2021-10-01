"""empty message

Revision ID: 29824df5c15c
Revises: d8c2fdb14c1b
Create Date: 2021-10-01 15:15:55.942824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29824df5c15c'
down_revision = 'd8c2fdb14c1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], name=op.f('fk_answer_voter_answer_id_answer'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_answer_voter_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'answer_id', name=op.f('pk_answer_voter'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer_voter')
    # ### end Alembic commands ###
