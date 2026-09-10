"""add locality coords and distances to rooms

Revision ID: 44b03d0b452e
Revises: d7a48a6eea8a
Create Date: 2026-09-10 23:51:49.635562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44b03d0b452e'
down_revision: Union[str, Sequence[str], None] = 'd7a48a6eea8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('rooms', sa.Column('locality', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('rooms', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('rooms', sa.Column('distance_campus', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('distance_mall', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('distance_market', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('distance_food', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('image_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('rooms', 'image_url')
    op.drop_column('rooms', 'distance_food')
    op.drop_column('rooms', 'distance_market')
    op.drop_column('rooms', 'distance_mall')
    op.drop_column('rooms', 'distance_campus')
    op.drop_column('rooms', 'longitude')
    op.drop_column('rooms', 'latitude')
    op.drop_column('rooms', 'locality')
