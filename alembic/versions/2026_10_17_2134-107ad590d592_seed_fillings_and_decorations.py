"""Seed fillings and decorations

Revision ID: 107ad590d592
Revises: 75b802ff518e
Create Date: 2026-10-17 21:34:41.507653

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "107ad590d592"
down_revision: Union[str, Sequence[str], None] = "75b802ff518e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

BASE_PRICE = 40

fillings = sa.table(
    "fillings",
    sa.column("name", sa.String),
    sa.column("price_per_kg", sa.Integer),
)
decorations = sa.table(
    "decorations",
    sa.column("name", sa.String),
    sa.column("price", sa.Integer),
)


def upgrade() -> None:
    op.alter_column("fillings", "id", server_default=sa.text("uuidv7()"))
    op.alter_column("decorations", "id", server_default=sa.text("uuidv7()"))
    op.bulk_insert(
        fillings,
        [
            {"name": "Сникерс", "price_per_kg": BASE_PRICE},
            {"name": "Красный бархат", "price_per_kg": BASE_PRICE + 5},
            {"name": "Манго-Маракуйя", "price_per_kg": BASE_PRICE + 8},
        ],
    )
    op.bulk_insert(
        decorations,
        [
            {"name": "Свежие ягоды", "price": 15},
            {"name": "Шоколадные фигуры", "price": 20},
            {"name": "Печать фото", "price": 10},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM decorations")
    op.execute("DELETE FROM fillings")
