"""empty message

Revision ID: cb57e8a0265d
Revises: d8aabeb2c3ed
Create Date: 2021-10-07 14:12:20.404592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb57e8a0265d'
down_revision = 'd8aabeb2c3ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], name=op.f('fk_board_voter_answer_id_answer'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_board_voter_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'answer_id', name=op.f('pk_board_voter'))
    )
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('hits')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hits', sa.INTEGER(), server_default=sa.text("'0'"), nullable=True))

    op.drop_table('board_voter')
    # ### end Alembic commands ###
