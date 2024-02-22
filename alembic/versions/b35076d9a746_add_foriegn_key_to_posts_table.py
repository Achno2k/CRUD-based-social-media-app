"""add foriegn-key to posts table

Revision ID: b35076d9a746
Revises: d0844c0636f2
Create Date: 2024-02-22 01:43:44.031949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b35076d9a746'
down_revision: Union[str, None] = 'd0844c0636f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fkey"
                          , source_table="posts"
                          , referent_table="users"
                          , local_cols=['owner_id']
                          , remote_cols=['id'], ondelete="CASCADE"
                        )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")
    
    pass
