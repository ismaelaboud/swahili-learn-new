"""Add course enrollment model

Revision ID: 12970368d66c
Revises: 71c55d96910f
Create Date: 2024-12-14 00:59:47.179574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12970368d66c'
down_revision: Union[str, None] = '71c55d96910f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enrollments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('enrolled_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'ACTIVE', 'COMPLETED', 'DROPPED', name='enrollmentstatus'), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enrollments_id'), 'enrollments', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_enrollments_id'), table_name='enrollments')
    op.drop_table('enrollments')
    # ### end Alembic commands ###
