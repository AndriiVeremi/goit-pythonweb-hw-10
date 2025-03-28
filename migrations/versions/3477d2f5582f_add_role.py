"""add role

Revision ID: 3477d2f5582f
Revises: 7ea2edf4820b
Create Date: 2025-03-27 21:01:57.081770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3477d2f5582f'
down_revision: Union[str, None] = '7ea2edf4820b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    stmt = "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole')"
    result = conn.execute(sa.text(stmt)).scalar()
    if not result:
        op.execute("CREATE TYPE userrole AS ENUM ('USER', 'MODERATOR', 'ADMIN')")

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("USER", "MODERATOR", "ADMIN", name="userrole"),
            nullable=True,
        ),
    )

    op.execute("UPDATE users SET role = 'USER' WHERE role IS NULL")

    op.alter_column("users", "role", nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "role")

    op.execute("DROP TYPE userrole")
    # ### end Alembic commands ###
