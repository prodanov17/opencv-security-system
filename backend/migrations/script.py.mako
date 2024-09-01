"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}
    op.add_column('camera', sa.Column('notification_enabled', sa.Boolean(), nullable=True, server_default='false'))



def downgrade():
    ${downgrades if downgrades else "pass"}
    op.drop_column('camera', 'notification_enabled')

