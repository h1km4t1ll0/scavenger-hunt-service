from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, UUID

from hunt.db import DeclarativeBase


class SolvedTasks(DeclarativeBase):
    __tablename__ = "solved_tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique index of element (type UUID)",
    )
    task_id = Column(
        "task_id",
        UUID(as_uuid=True),
        nullable=False,
        unique=False,
    )
    team_id = Column("team_id", UUID(as_uuid=True), nullable=False, unique=False)

    def __repr__(self) -> str:
        return f"task id: : {self.task_id}\n" f"team id: {self.team_id}\n"
