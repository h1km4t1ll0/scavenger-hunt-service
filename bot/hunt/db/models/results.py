from sqlalchemy import CheckConstraint, Column, func
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, UUID, BOOLEAN
from sqlalchemy.orm import Session

from hunt.db import DeclarativeBase, get_db


class Results(DeclarativeBase):
    __tablename__ = "results"

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    team_id = Column(
        "team_id",
        UUID(as_uuid=True),
        nullable=False,
        unique=False,
    )
    task_id = Column(
        "task_id",
        UUID(as_uuid=True),
        nullable=False,
        unique=False,
    )
    amount = Column("amount", INTEGER, default=0)

    def __repr__(self) -> str:
        return (
            f"name: {self.name}\n"
            f"amount: {self.amount}\n"
            f"members: {self.member_number}\n"
            f"id: {self.id}\n"
            f"token: {self.token}\n"
        )

    @classmethod
    def write(cls, db: Session, team_id, task_id, amount: int) -> None:
        result: cls = db.query(cls).filter_by(team_id=team_id, task_id=task_id).first()
        if result is None:
            result: cls = cls(team_id=team_id, task_id=task_id, amount=amount)
            db.add(result)
        else:
            result.amount += amount
        db.commit()
        db.refresh(result)

    @classmethod
    def get(cls, db: Session, **kwargs):
        db_user: cls = db.query(cls).filter_by(**kwargs).first()
        return db_user
