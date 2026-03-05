"""add_user_patronomic

Revision ID: 22bab317cab9
Revises: 8dce2910ff8b
Create Date: 2026-03-06 00:24:54.334274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22bab317cab9'
down_revision: Union[str, Sequence[str], None] = '8dce2910ff8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
