"""tets multiple images

Revision ID: 160fc5529ae4
Revises: 5af3fc42b58f
Create Date: 2018-06-14 08:27:58.232124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '160fc5529ae4'
down_revision = '5af3fc42b58f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posttest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_photo',
    sa.Column('width', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('mimetype', sa.String(length=255), nullable=False),
    sa.Column('original', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('order_index', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posttest.id'], ),
    sa.PrimaryKeyConstraint('width', 'height', 'post_id', 'order_index')
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
    op.drop_table('post_photo')
    op.drop_table('posttest')
    # ### end Alembic commands ###
