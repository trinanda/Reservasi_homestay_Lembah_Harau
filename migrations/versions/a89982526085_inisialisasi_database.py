"""inisialisasi database

Revision ID: a89982526085
Revises: 
Create Date: 2018-05-25 18:44:11.494074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a89982526085'
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
    sa.Column('status_pembayaran', sa.Enum('pending', 'confirmed', 'rejected', name='status_pembayaran'), nullable=True),
    sa.PrimaryKeyConstraint('nomor_invoice'),
    sa.UniqueConstraint('nomor_invoice')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Invoice')
    # ### end Alembic commands ###
