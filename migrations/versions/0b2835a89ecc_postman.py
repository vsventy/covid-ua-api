"""empty message

Revision ID: 0b2835a89ecc
Revises: ad08a8379c12
Create Date: 2020-05-21 12:09:21.130534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b2835a89ecc'
down_revision = 'ad08a8379c12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('postman_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('api_token', sa.String(length=100), nullable=False),
    sa.Column('service_type', sa.Enum('EMAIL', 'SMS', 'TELEGRAM', 'VIBER', name='servicetype'), nullable=False),
    sa.Column('notify_type', sa.Enum('TEXT', 'TEMPLATE', name='notifytype'), nullable=False),
    sa.Column('template_key', sa.String(length=100), nullable=True),
    sa.Column('message_text', sa.String(length=1000), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_token')
    )
    op.add_column('user', sa.Column('phone', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone')
    op.drop_table('postman_notification')
    # ### end Alembic commands ###
