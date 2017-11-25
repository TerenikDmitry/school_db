"""empty message

Revision ID: f90443b2e270
Revises: e8d8e3a22ab8
Create Date: 2017-11-25 17:40:52.605413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f90443b2e270'
down_revision = 'e8d8e3a22ab8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers_classroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('classroom_id', sa.Integer(), nullable=True),
    sa.Column('user_id_teacher', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ),
    sa.ForeignKeyConstraint(['user_id_teacher'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('classroom_id'),
    sa.UniqueConstraint('user_id_teacher')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teachers_classroom')
    # ### end Alembic commands ###
