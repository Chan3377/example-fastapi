"""add content column to posts table

Revision ID: 02d5ebc9e352
Revises: 285a8fee9181
Create Date: 2023-12-03 14:12:44.956657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "02d5ebc9e352"
down_revision: Union[str, None] = "285a8fee9181"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
