"""inisialisasi database

Revision ID: 86ee228966c5
Revises: 
Create Date: 2018-06-10 20:21:30.046249

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry


# revision identifiers, used by Alembic.
revision = '86ee228966c5'
down_revision = None
branch_labels = None
depends_on = None

from sqlalchemy.dialects.postgresql import ENUM
status_pembayaran = ENUM('pending', 'confirmed', 'rejected', name='status_pembayaran', create_type=False)

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kamar',
    sa.Column('id_kamar', sa.Integer(), nullable=False),
    sa.Column('nama_kamar', sa.String(), nullable=True),
    sa.Column('lokasi', Geometry(geometry_type='POINT'), nullable=True),
    sa.Column('keterangan_kamar', sa.String(), nullable=True),
    sa.Column('room_images', sa.Unicode(length=128), nullable=True),
    sa.Column('harga_kamar', sa.Integer(), nullable=True),
    sa.Column('urutan_kamar', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id_kamar')
    )
    op.create_table('invoice',
    sa.Column('nomor_invoice', sa.String(), nullable=False),
    sa.Column('nama_pemesan', sa.String(length=15), nullable=True),
    sa.Column('nomor_telepon', sa.Numeric(), nullable=True),
    sa.Column('email_pemesan', sa.String(), nullable=True),
    sa.Column('nama_kamar', sa.String(), nullable=True),
    sa.Column('lama_menginap', sa.Integer(), nullable=True),
    sa.Column('harga_total_pemesan_kamar', sa.Integer(), nullable=True),
    sa.Column('tanggal_pemesanan', sa.DateTime(), nullable=True),
    sa.Column('kamar_id', sa.Integer(), nullable=False),
    sa.Column('status_pembayaran', status_pembayaran, nullable=True),
    sa.ForeignKeyConstraint(['kamar_id'], ['kamar.id_kamar'], ),
    sa.PrimaryKeyConstraint('nomor_invoice'),
    sa.UniqueConstraint('nomor_invoice')
    )
    # op.drop_table('spatial_ref_sys')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    op.drop_table('invoice')
    op.drop_table('kamar')
    # ### end Alembic commands ###