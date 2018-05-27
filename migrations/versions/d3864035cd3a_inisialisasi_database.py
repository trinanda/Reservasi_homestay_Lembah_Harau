"""inisialisasi database

Revision ID: d3864035cd3a
Revises: 
Create Date: 2018-05-27 16:43:33.445742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3864035cd3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Invoice',
    sa.Column('nomor_invoice', sa.String(), nullable=False),
    sa.Column('nama_pemesan', sa.String(length=15), nullable=True),
    sa.Column('nomor_telepon', sa.Numeric(), nullable=True),
    sa.Column('email_pemesan', sa.String(), nullable=True),
    sa.Column('nama_kamar', sa.String(), nullable=True),
    sa.Column('lama_menginap', sa.Integer(), nullable=True),
    sa.Column('harga_total_pemesan_kamar', sa.Integer(), nullable=True),
    sa.Column('tanggal_pemesanan', sa.DateTime(), nullable=True),
    sa.Column('status_pembayaran', sa.Enum('pending', 'confirmed', 'rejected', name='status_pembayaran'), nullable=True),
    sa.PrimaryKeyConstraint('nomor_invoice'),
    sa.UniqueConstraint('nomor_invoice')
    )
    op.create_table('kamar',
    sa.Column('id_kamar', sa.Integer(), nullable=False),
    sa.Column('nama_kamar', sa.String(), nullable=True),
    sa.Column('room_description', sa.String(), nullable=True),
    sa.Column('room_images', sa.Unicode(length=128), nullable=True),
    sa.Column('harga_kamar', sa.Integer(), nullable=True),
    sa.Column('urutan_kamar', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id_kamar')
    )
    op.create_table('page',
    sa.Column('id_halaman', sa.Integer(), nullable=False),
    sa.Column('judul', sa.String(), nullable=True),
    sa.Column('tag', sa.String(), nullable=True),
    sa.Column('konten', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id_halaman')
    )
    op.create_table('menu',
    sa.Column('id_menu', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('urutan', sa.Integer(), nullable=True),
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['page.id_halaman'], ),
    sa.PrimaryKeyConstraint('id_menu')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu')
    op.drop_table('page')
    op.drop_table('kamar')
    op.drop_table('Invoice')
    # ### end Alembic commands ###
