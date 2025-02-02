"""Add unique constraints

Revision ID: b2fa308044b5
Revises: 0b8757876a7c
Create Date: 2024-01-26 13:31:14.797548

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from loguru import logger  # noqa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "b2fa308044b5"
down_revision: Union[str, None] = "0b8757876a7c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = sa.inspect(conn)  # type: ignore
    tables = inspector.get_table_names()
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        if "flowstyle" in tables:
            op.drop_table("flowstyle")
        with op.batch_alter_table("flow", schema=None) as batch_op:
            flow_columns = [column["name"] for column in inspector.get_columns("flow")]
            if "is_component" not in flow_columns:
                batch_op.add_column(sa.Column("is_component", sa.Boolean(), nullable=True))
            if "updated_at" not in flow_columns:
                batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
            if "folder" not in flow_columns:
                batch_op.add_column(sa.Column("folder", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
            if "user_id" not in flow_columns:
                batch_op.add_column(sa.Column("user_id", sqlmodel.sql.sqltypes.types.Uuid(), nullable=True))

            indices = inspector.get_indexes("flow")
            indices_names = [index["name"] for index in indices]
            if "ix_flow_user_id" not in indices_names:
                batch_op.create_index(batch_op.f("ix_flow_user_id"), ["user_id"], unique=False)

            # Check for existing foreign key constraints
            constraints = inspector.get_foreign_keys("flow")
            constraint_names = [constraint["name"] for constraint in constraints]

            if "fk_flow_user_id_user" not in constraint_names:
                batch_op.create_foreign_key("fk_flow_user_id_user", "user", ["user_id"], ["id"])

    except Exception as e:
        logger.exception(f"Error during upgrade: {e}")
        pass


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)  # type: ignore
    try:
        # Re-create the dropped table 'flowstyle' if it was previously dropped in upgrade
        if "flowstyle" not in inspector.get_table_names():
            op.create_table(
                "flowstyle",
                sa.Column("color", sa.String(), nullable=False),
                sa.Column("emoji", sa.String(), nullable=False),
                sa.Column("flow_id", sqlmodel.sql.sqltypes.types.Uuid(), nullable=True),
                sa.Column("id", sqlmodel.sql.sqltypes.types.Uuid(), nullable=False),
                sa.ForeignKeyConstraint(["flow_id"], ["flow.id"]),
                sa.PrimaryKeyConstraint("id"),
                sa.UniqueConstraint("id"),
            )

        with op.batch_alter_table("flow", schema=None) as batch_op:
            # Check and remove newly added columns and constraints in upgrade
            flow_columns = [column["name"] for column in inspector.get_columns("flow")]
            if "user_id" in flow_columns:
                batch_op.drop_column("user_id")
            if "folder" in flow_columns:
                batch_op.drop_column("folder")
            if "updated_at" in flow_columns:
                batch_op.drop_column("updated_at")
            if "is_component" in flow_columns:
                batch_op.drop_column("is_component")

            indices = inspector.get_indexes("flow")
            indices_names = [index["name"] for index in indices]
            if "ix_flow_user_id" in indices_names:
                batch_op.drop_index("ix_flow_user_id")
            # Assuming fk_flow_user_id_user is a foreign key constraint's name, not an index
            constraints = inspector.get_foreign_keys("flow")
            constraint_names = [constraint["name"] for constraint in constraints]
            if "fk_flow_user_id_user" in constraint_names:
                batch_op.drop_constraint("fk_flow_user_id_user", type_="foreignkey")

    except Exception as e:
        # It's generally a good idea to log the exception or handle it in a way other than a bare pass
        print(f"Error during downgrade: {e}")
