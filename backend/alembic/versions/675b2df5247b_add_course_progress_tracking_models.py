"""Add course progress tracking models

Revision ID: 675b2df5247b
Revises: 12970368d66c
Create Date: 2024-12-14 01:09:18.559721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '675b2df5247b'
down_revision: Union[str, None] = '12970368d66c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    if not sa.inspect(op.get_bind()).has_table('lessons'):
        op.create_table('lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.Column('content_type', sa.String(), nullable=True),
        sa.Column('content_url', sa.String(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)

    if not sa.inspect(op.get_bind()).has_table('course_progresses'):
        op.create_table('course_progresses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('enrollment_id', sa.Integer(), nullable=True),
        sa.Column('lesson_id', sa.Integer(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('progress_percentage', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['enrollment_id'], ['enrollments.id'], ),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_course_progresses_id'), 'course_progresses', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_course_progresses_id'), table_name='course_progresses')
    op.drop_table('course_progresses')
    op.drop_index(op.f('ix_lessons_id'), table_name='lessons')
    op.drop_table('lessons')
    # ### end Alembic commands ###
