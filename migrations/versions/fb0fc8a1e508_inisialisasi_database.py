"""inisialisasi database

Revision ID: fb0fc8a1e508
Revises: 
Create Date: 2018-05-31 12:25:01.234852

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fb0fc8a1e508'
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
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('send_email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('send_email')
    )
    op.create_table('menu',
    sa.Column('id_menu', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('urutan', sa.Integer(), nullable=True),
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['page.id_halaman'], ),
    sa.PrimaryKeyConstraint('id_menu')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.add_column('Invoice', sa.Column('status_pembayaran', sa.Enum('pending', 'confirmed', 'rejected', name='status_pembayaran'), nullable=True))
    op.create_unique_constraint(None, 'Invoice', ['nomor_invoice'])
    op.drop_column('Invoice', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Invoice', sa.Column('status', postgresql.ENUM('pending', 'confirmed', 'rejected', name='status'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Invoice', type_='unique')
    op.drop_column('Invoice', 'status_pembayaran')
    op.drop_table('roles_users')
    op.drop_table('menu')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('page')
    op.drop_table('kamar')
    # ### end Alembic commands ###