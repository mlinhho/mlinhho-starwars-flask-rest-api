"""empty message

Revision ID: c3cfcb8771d0
Revises: 0b1cd2baa2af
Create Date: 2023-05-06 00:45:24.663235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3cfcb8771d0'
down_revision = '0b1cd2baa2af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=40), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###