"""Added unique constraint in name column products table

Revision ID: 9dc892597f76
Revises: 9cb8b13b566a
Create Date: 2025-06-17 16:57:58.390398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dc892597f76'
down_revision: Union[str, None] = '9cb8b13b566a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'products', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    # ### end Alembic commands ###
