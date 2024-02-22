"""add column content to posts table

Revision ID: 76ddef27fd08
Revises: 5ba681b64fd5
Create Date: 2024-02-22 01:23:40.165604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76ddef27fd08'
down_revision: Union[str, None] = '5ba681b64fd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
