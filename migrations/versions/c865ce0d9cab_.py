"""empty message

Revision ID: c865ce0d9cab
Revises: d184087adf0f
Create Date: 2021-11-25 11:56:10.515668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c865ce0d9cab'
down_revision = 'd184087adf0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_user')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tel', sa.String(length=50), server_default='01022369764', nullable=True))
        batch_op.drop_column('number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number', sa.VARCHAR(length=50), server_default=sa.text("'01022369764'"), nullable=False))
        batch_op.drop_column('tel')

    op.create_table('_alembic_tmp_user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('tel', sa.VARCHAR(length=50), server_default=sa.text("'01022369764'"), nullable=True),
    sa.Column('username', sa.VARCHAR(length=150), nullable=False),
    sa.Column('password', sa.VARCHAR(length=200), nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('fir_joo', sa.VARCHAR(length=6), server_default=sa.text("'980109'"), nullable=False),
    sa.Column('sec_joo', sa.VARCHAR(length=7), server_default=sa.text("'1157119'"), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_user'),
    sa.UniqueConstraint('email', name='uq_user_email'),
    sa.UniqueConstraint('sec_joo', name='uq_user_sec_joo'),
    sa.UniqueConstraint('username', name='uq_user_username')
    )
    # ### end Alembic commands ###
