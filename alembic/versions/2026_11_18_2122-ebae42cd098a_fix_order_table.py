"""fix order table

Revision ID: ebae42cd098a
Revises: b92b99679058
Create Date: 2026-11-18 21:22:51.922495

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ebae42cd098a"
down_revision: Union[str, Sequence[str], None] = "b92b99679058"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("orders", sa.Column("recipe_id", sa.Uuid(), nullable=True))
    op.alter_column("orders", "filling_id", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key(
        op.f("fk_orders_recipe_id_recipes"),
        "orders",
        "recipes",
        ["recipe_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_orders_recipe_id_recipes"), "orders", type_="foreignkey"
    )
    op.alter_column("orders", "filling_id", existing_type=sa.UUID(), nullable=False)
    op.drop_column("orders", "recipe_id")
