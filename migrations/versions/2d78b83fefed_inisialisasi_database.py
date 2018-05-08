"""inisialisasi database

Revision ID: 2d78b83fefed
Revises: 
Create Date: 2018-05-05 09:14:23.117347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d78b83fefed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###