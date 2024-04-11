from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, UUID

from hunt.db import DeclarativeBase


class SolvedQuiz(DeclarativeBase):
    __tablename__ = "solved_quiz"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique index of element (type UUID)",
    )
    team_id = Column("team_id", UUID(as_uuid=True), nullable=False, unique=False)
    amount = Column("points", INTEGER, default=0)
