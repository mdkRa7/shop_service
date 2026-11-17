"""add order number

Revision ID: 4761d2cee5af
Revises: 107ad590d592
Create Date: 2026-11-10 23:29:24.685157

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4761d2cee5af"
down_revision: Union[str, Sequence[str], None] = "107ad590d592"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "orders",
        sa.Column("number", sa.Integer(), sa.Identity(always=False), nullable=False),
    )
    op.create_unique_constraint(op.f("uq_orders_number"), "orders", ["number"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_orders_number"), "orders", type_="unique")
    op.drop_column("orders", "number")
