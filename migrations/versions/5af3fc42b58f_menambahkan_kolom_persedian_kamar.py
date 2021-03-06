"""menambahkan kolom persedian kamar

Revision ID: 5af3fc42b58f
Revises: 86ee228966c5
Create Date: 2018-06-13 12:31:18.411720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5af3fc42b58f'
down_revision = '86ee228966c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    op.create_unique_constraint(None, 'invoice', ['nomor_invoice'])
    op.add_column('kamar', sa.Column('kamar_tersedia', sa.Integer(), nullable=True))
    op.drop_index('idx_kamar_lokasi', table_name='kamar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_kamar_lokasi', 'kamar', ['lokasi'], unique=False)
    op.drop_column('kamar', 'kamar_tersedia')
    op.drop_constraint(None, 'invoice', type_='unique')
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    # ### end Alembic commands ###
