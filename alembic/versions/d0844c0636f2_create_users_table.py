"""create users table

Revision ID: d0844c0636f2
Revises: 76ddef27fd08
Create Date: 2024-02-22 01:35:57.877031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd0844c0636f2'
down_revision: Union[str, None] = '76ddef27fd08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users"
                     , sa.Column("id", sa.Integer(), nullable=False, primary_key=True, unique=True)
                     , sa.Column("email", sa.String(), nullable=False, unique=True)
                     , sa.Column("password", sa.String(), nullable=False)
                     , sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
