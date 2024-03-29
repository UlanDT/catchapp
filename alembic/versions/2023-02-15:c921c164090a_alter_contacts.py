"""alter contacts

Revision ID: c921c164090a
Revises: 1ea9b17deeac
Create Date: 2023-02-15 02:46:37.770788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c921c164090a'
down_revision = '1ea9b17deeac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('contacts', sa.Column('contact_id', sa.Integer(), nullable=False))
    op.drop_constraint('_user_id_uc', 'contacts', type_='unique')
    op.create_unique_constraint('_user_id_uc', 'contacts', ['user_id', 'contact_id'])
    op.drop_constraint('contacts_user_id1_fkey', 'contacts', type_='foreignkey')
    op.drop_constraint('contacts_user_id2_fkey', 'contacts', type_='foreignkey')
    op.create_foreign_key(None, 'contacts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'contacts', 'users', ['contact_id'], ['id'], ondelete='CASCADE')
    op.drop_column('contacts', 'user_id2')
    op.drop_column('contacts', 'user_id1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('user_id1', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('contacts', sa.Column('user_id2', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.create_foreign_key('contacts_user_id2_fkey', 'contacts', 'users', ['user_id2'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('contacts_user_id1_fkey', 'contacts', 'users', ['user_id1'], ['id'], ondelete='CASCADE')
    op.drop_constraint('_user_id_uc', 'contacts', type_='unique')
    op.create_unique_constraint('_user_id_uc', 'contacts', ['user_id1', 'user_id2'])
    op.drop_column('contacts', 'contact_id')
    op.drop_column('contacts', 'user_id')
    # ### end Alembic commands ###
