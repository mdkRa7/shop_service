"""add unique name

Revision ID: b92b99679058
Revises: 2356b4b7875f
Create Date: 2026-11-18 20:15:25.639406

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b92b99679058"
down_revision: Union[str, Sequence[str], None] = "2356b4b7875f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(op.f("uq_recipes_name"), "recipes", ["name"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_recipes_name"), "recipes", type_="unique")
