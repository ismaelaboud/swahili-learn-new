"""Add lesson visibility controls

Revision ID: f0b5d2235f06
Revises: 675b2df5247b
Create Date: 2024-12-19 16:41:47.380336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f0b5d2235f06'
down_revision: Union[str, None] = '675b2df5247b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safely check if the table exists before adding columns
    inspector = sa.inspect(op.get_bind())
    columns = inspector.get_columns('lesson_modules')
    existing_columns = [col['name'] for col in columns]

    with op.batch_alter_table('lesson_modules', schema=None) as batch_op:
        # Add is_visible column if not exists
        if 'is_visible' not in existing_columns:
            batch_op.add_column(sa.Column('is_visible', sa.Boolean(), nullable=False, server_default='true'))
        
        # Add visibility_start_date column if not exists
        if 'visibility_start_date' not in existing_columns:
            batch_op.add_column(sa.Column('visibility_start_date', sa.DateTime(), nullable=True))
        
        # Add visibility_end_date column if not exists
        if 'visibility_end_date' not in existing_columns:
            batch_op.add_column(sa.Column('visibility_end_date', sa.DateTime(), nullable=True))
        
        # Add required_roles column if not exists
        if 'required_roles' not in existing_columns:
            batch_op.add_column(sa.Column('required_roles', 
                postgresql.ARRAY(sa.String()), 
                nullable=False, 
                server_default=sa.text("ARRAY['student']::text[]")
            ))


def downgrade() -> None:
    # Remove added columns in reverse order
    with op.batch_alter_table('lesson_modules', schema=None) as batch_op:
        batch_op.drop_column('required_roles')
        batch_op.drop_column('visibility_end_date')
        batch_op.drop_column('visibility_start_date')
        batch_op.drop_column('is_visible')
