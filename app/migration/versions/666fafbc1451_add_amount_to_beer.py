"""add amount to Beer

Revision ID: 666fafbc1451
Revises: 87493d6fed7d
Create Date: 2023-05-09 22:12:26.551717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '666fafbc1451'
down_revision = '87493d6fed7d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('beer', sa.Column('amount', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_beer_amount'), 'beer', ['amount'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_beer_amount'), table_name='beer')
    op.drop_column('beer', 'amount')
    # ### end Alembic commands ###