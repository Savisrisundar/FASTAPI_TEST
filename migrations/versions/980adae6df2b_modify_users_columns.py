"""Modify Users Columns

Revision ID: 980adae6df2b
Revises: 14e0c88a971f
Create Date: 2023-09-07 09:59:29.057871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '980adae6df2b'
down_revision = '14e0c88a971f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fullname', sa.String(), nullable=True))
    op.drop_index('ix_users_full_name', table_name='users')
    op.create_index(op.f('ix_users_fullname'), 'users', ['fullname'], unique=False)
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_fullname'), table_name='users')
    op.create_index('ix_users_full_name', 'users', ['full_name'], unique=False)
    op.drop_column('users', 'fullname')
    # ### end Alembic commands ###