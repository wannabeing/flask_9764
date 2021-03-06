"""empty message

Revision ID: ca88f1392c6a
Revises: 266f5aba65fa
Create Date: 2021-10-06 14:06:45.704938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca88f1392c6a'
down_revision = '266f5aba65fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('fk_comment_board_id_question', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_comment_board_id_board'), 'board', ['board_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_comment_board_id_board'), type_='foreignkey')
        batch_op.create_foreign_key('fk_comment_board_id_question', 'question', ['board_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###
