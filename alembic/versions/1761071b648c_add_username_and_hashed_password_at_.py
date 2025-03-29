"""Add username and hashed_password at customers table

Revision ID: 1761071b648c
Revises: 5a6d0f8d948e
Create Date: 2025-03-23 13:21:00.705935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1761071b648c'
down_revision: Union[str, None] = '5a6d0f8d948e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("customers", sa.Column('username', sa.String(255), nullable=True))
    op.add_column("customers", sa.Column('hashed_password', sa.Text(), nullable=True))
    op.create_unique_constraint("uq_customers_username", "customers", ["username"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("customers", "username")
    op.drop_column("customers", "hashed_password")
