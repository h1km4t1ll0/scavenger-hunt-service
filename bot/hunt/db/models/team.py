from sqlalchemy import CheckConstraint, Column, func
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, UUID, BOOLEAN
from sqlalchemy.orm import Session

from hunt.db import DeclarativeBase, get_db


class Team(DeclarativeBase):
    __tablename__ = "team"

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    token = Column(
        "token",
        TEXT,
        nullable=False,
        unique=True,
    )
    amount = Column("amount", INTEGER, default=0)
    name = Column("name", TEXT, nullable=True, unique=True)
    member_number = Column(
        "member_number",
        INTEGER,
        default=0,
        doc="Contains current number of group members. Updates after adding new member to group",
    )
    visible = Column(
        "visible",
        BOOLEAN,
        default=True,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"name: {self.name}\n"
            f"amount: {self.amount}\n"
            f"members: {self.member_number}\n"
            f"id: {self.id}\n"
            f"token: {self.token}\n"
        )

    @classmethod
    def give_money(cls, db: Session, id, amount: int) -> int:
        db_team: cls = db.query(cls).where(cls.id == id).first
        db_team.amount += amount
        db.commit()
        db.refresh(db_team)
        return db_team.amount

    @classmethod
    def get(cls, db: Session, **kwargs):
        db_user: cls = db.query(cls).filter_by(**kwargs).first()
        return db_user

    def __lt__(self, other):
        return self.amount < other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __eq__(self, other):
        return self.amount == other.amount
