"""add Purchase and DrinkRecord

Revision ID: 87493d6fed7d
Revises: 507faa167c4d
Create Date: 2023-05-06 20:28:53.671435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87493d6fed7d'
down_revision = '507faa167c4d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('beer_id', sa.Integer(), nullable=True),
    sa.Column('date_purchase', sa.Date(), nullable=True),
    sa.Column('date_untapped', sa.Date(), nullable=True),
    sa.Column('date_emptied', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['beer_id'], ['beer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_date_emptied'), 'purchase', ['date_emptied'], unique=False)
    op.create_index(op.f('ix_purchase_date_purchase'), 'purchase', ['date_purchase'], unique=False)
    op.create_index(op.f('ix_purchase_date_untapped'), 'purchase', ['date_untapped'], unique=False)
    op.create_index(op.f('ix_purchase_description'), 'purchase', ['description'], unique=False)
    op.create_table('drink_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True, comment='Amount to drink'),
    sa.Column('purchase_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['purchase_id'], ['purchase.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_drink_record_date'), 'drink_record', ['date'], unique=False)
    op.create_index(op.f('ix_drink_record_description'), 'drink_record', ['description'], unique=False)
    op.add_column('beer', sa.Column('price_jpy', sa.Integer(), nullable=True))
    op.add_column('beer', sa.Column('price', sa.Float(), nullable=True))
    op.add_column('beer', sa.Column('currency', sa.String(), nullable=True))
    op.create_index(op.f('ix_beer_currency'), 'beer', ['currency'], unique=False)
    op.create_index(op.f('ix_beer_price'), 'beer', ['price'], unique=False)
    op.create_index(op.f('ix_beer_price_jpy'), 'beer', ['price_jpy'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_beer_price_jpy'), table_name='beer')
    op.drop_index(op.f('ix_beer_price'), table_name='beer')
    op.drop_index(op.f('ix_beer_currency'), table_name='beer')
    op.drop_column('beer', 'currency')
    op.drop_column('beer', 'price')
    op.drop_column('beer', 'price_jpy')
    op.drop_index(op.f('ix_drink_record_description'), table_name='drink_record')
    op.drop_index(op.f('ix_drink_record_date'), table_name='drink_record')
    op.drop_table('drink_record')
    op.drop_index(op.f('ix_purchase_description'), table_name='purchase')
    op.drop_index(op.f('ix_purchase_date_untapped'), table_name='purchase')
    op.drop_index(op.f('ix_purchase_date_purchase'), table_name='purchase')
    op.drop_index(op.f('ix_purchase_date_emptied'), table_name='purchase')
    op.drop_table('purchase')
    # ### end Alembic commands ###
