"""create post table

Revision ID: 4a43d3a873e2
Revises: a76b366ba9b3
Create Date: 2022-12-19 12:23:27.772594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a43d3a873e2'
down_revision = 'a76b366ba9b3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
