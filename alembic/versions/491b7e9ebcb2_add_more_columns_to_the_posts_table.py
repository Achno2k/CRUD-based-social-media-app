"""add more columns to the posts table

Revision ID: 491b7e9ebcb2
Revises: b35076d9a746
Create Date: 2024-02-22 01:50:01.000191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '491b7e9ebcb2'
down_revision: Union[str, None] = 'b35076d9a746'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, default=True))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")

    pass
