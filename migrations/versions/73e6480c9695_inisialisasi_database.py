"""inisialisasi database

Revision ID: 73e6480c9695
Revises: 
Create Date: 2018-06-09 17:22:25.722665

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry

# revision identifiers, used by Alembic.
revision = '73e6480c9695'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('point', Geometry(geometry_type='POINT'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.alter_column('invoice', 'kamar_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoice', 'kamar_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('map')
    # ### end Alembic commands ###
