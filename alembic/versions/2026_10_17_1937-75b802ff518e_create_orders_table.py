"""Create orders table

Revision ID: 75b802ff518e
Revises: c78b977f5e42
Create Date: 2026-10-17 19:37:36.117152

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "75b802ff518e"
down_revision: Union[str, Sequence[str], None] = "c78b977f5e42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("customer_name", sa.String(length=100), nullable=False),
        sa.Column("inscription", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("filling_id", sa.Uuid(), nullable=False),
        sa.Column("decoration_id", sa.Uuid(), nullable=True),
        sa.Column("total_price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("pickup_date", sa.Date(), nullable=False),
        sa.Column("weight_kg", sa.Numeric(precision=4, scale=2), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "new",
                "confirmed",
                "ready",
                "done",
                "cancelled",
                name="orderstatus",
            ),
            server_default="new",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["decoration_id"],
            ["decorations.id"],
            name=op.f("fk_orders_decoration_id_decorations"),
        ),
        sa.ForeignKeyConstraint(
            ["filling_id"],
            ["fillings.id"],
            name=op.f("fk_orders_filling_id_fillings"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )
    op.create_index(
        op.f("ix_orders_pickup_date"), "orders", ["pickup_date"], unique=False
    )
    op.create_index(op.f("ix_orders_user_id"), "orders", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_orders_user_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_pickup_date"), table_name="orders")
    op.drop_table("orders")
