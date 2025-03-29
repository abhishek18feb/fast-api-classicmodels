"""Add username and hashed_password at employess table

Revision ID: 5a6d0f8d948e
Revises: 
Create Date: 2025-03-23 13:01:23.195743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a6d0f8d948e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("employees", sa.Column('username', sa.String(255), nullable=True))
    op.add_column("employees", sa.Column('hashed_password', sa.Text(), nullable=True))
    op.create_unique_constraint("uq_employees_username", "employees", ["username"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("employees", "username")
    op.drop_column("employees", "hashed_password")
