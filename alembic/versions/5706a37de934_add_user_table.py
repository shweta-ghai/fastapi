"""add user table

Revision ID: 5706a37de934
Revises: bd5c92360905
Create Date: 2022-12-19 12:35:38.766251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5706a37de934'
down_revision = 'bd5c92360905'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass