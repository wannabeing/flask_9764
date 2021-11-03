"""empty message

Revision ID: d46f10cf9aba
Revises: 494518737349
Create Date: 2021-10-08 10:29:43.183557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd46f10cf9aba'
down_revision = '494518737349'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer_id', sa.Integer(), nullable=True))
        batch_op.alter_column('board_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(batch_op.f('fk_comment_answer_id_answer'), 'answer', ['answer_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_comment_answer_id_answer'), type_='foreignkey')
        batch_op.alter_column('board_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('answer_id')

    # ### end Alembic commands ###