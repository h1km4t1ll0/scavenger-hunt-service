from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, UUID, BOOLEAN, BIGINT
from sqlalchemy.orm import Session

from hunt.db import DeclarativeBase


class Task(DeclarativeBase):
    __tablename__ = "task"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique index of element (type UUID)",
    )
    name = Column("name", TEXT, nullable=True, unique=True)
    description = Column(
        "description",
        TEXT,
        nullable=True,
        unique=False,
    )
    type = Column(
        "type",
        TEXT,
        nullable=False,
        unique=False,
    )
    image = Column(
        "image",
        TEXT,
        nullable=True,
    )
    flag = Column(
        "flag",
        TEXT,
        nullable=True,
        unique=True,
    )
    with_manager = Column("with_manager", BOOLEAN, nullable=False)
    manager_id = Column("manager_id", BIGINT, nullable=True)
    amount = Column("amount", INTEGER, default=0)
    usage = Column(
        "usage",
        INTEGER,
        default=100000,
    )

    def __repr__(self) -> str:
        return (
            f"name: {self.name}\n"
            f"description: {self.description}\n"
            f"amount: {self.amount}\n"
            f"usage: {self.usage}\n"
            f"flag: {self.flag}\n"
            f"id: {self.id}\n"
        )

    @classmethod
    def get(cls, db: Session, **kwargs):
        db_task: cls = db.query(cls).filter_by(**kwargs).first()
        return db_task

    @classmethod
    def get_all(cls, db: Session, **kwargs):
        db_task: cls = db.query(cls).filter_by(**kwargs).all()
        return db_task if db_task is not None else []
