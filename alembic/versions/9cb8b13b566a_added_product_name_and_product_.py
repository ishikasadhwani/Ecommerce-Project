"""Added product_name and product_description  in order_items table

Revision ID: 9cb8b13b566a
Revises: b04ccb50e050
Create Date: 2025-06-16 23:33:19.741633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cb8b13b566a'
down_revision: Union[str, None] = 'b04ccb50e050'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('product_name', sa.String(), nullable=False))
    op.add_column('order_items', sa.Column('product_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_items', 'product_description')
    op.drop_column('order_items', 'product_name')
    # ### end Alembic commands ###
