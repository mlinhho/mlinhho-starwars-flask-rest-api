"""empty message

Revision ID: 0b1cd2baa2af
Revises: 8d62008ce55c
Create Date: 2023-05-06 00:16:11.073136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b1cd2baa2af'
down_revision = '8d62008ce55c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.String(length=40), nullable=True),
    sa.Column('climate', sa.String(length=50), nullable=True),
    sa.Column('terrain', sa.String(length=50), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('edited', sa.Date(), nullable=True),
    sa.Column('created', sa.Date(), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('birth_year', sa.Date(), nullable=True),
    sa.Column('eye_color', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('hair_color', sa.String(length=20), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('skin_color', sa.String(length=30), nullable=True),
    sa.Column('edited', sa.Date(), nullable=True),
    sa.Column('created', sa.Date(), nullable=False),
    sa.Column('origin_planet_url', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['origin_planet_url'], ['planet.url'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('password')
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('username')

    op.drop_table('favorite')
    op.drop_table('person')
    op.drop_table('planet')
    # ### end Alembic commands ###
