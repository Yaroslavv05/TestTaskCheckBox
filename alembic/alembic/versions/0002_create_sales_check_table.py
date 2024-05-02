from alembic import op
import sqlalchemy as sa


revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('price', sa.Float)
    )
    
    op.create_table(
        'sales_checks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('payment_type', sa.String),
        sa.Column('payment_amount', sa.Float)
    )

    op.create_table(
        'sales_check_products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sales_check_id', sa.Integer, sa.ForeignKey('sales_checks.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
        sa.Column('quantity', sa.Float),
        sa.Column('total', sa.Float)
    )


def downgrade():
    op.drop_table('products')
    op.drop_table('sales_check_products')
    op.drop_table('sales_checks')
