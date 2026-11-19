"""add is active to recipe

Revision ID: 2c06bacc9520
Revises: ebae42cd098a
Create Date: 2026-11-18 23:02:28.617175

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2c06bacc9520"
down_revision: Union[str, Sequence[str], None] = "ebae42cd098a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "recipes",
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("recipes", "is_active")
