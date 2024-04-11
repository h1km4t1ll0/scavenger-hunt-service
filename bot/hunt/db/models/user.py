from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, UUID
from sqlalchemy.orm import Session

from hunt.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "user"

    chat_id = Column(
        "chat_id",
        BIGINT,
        primary_key=True,
        unique=True,
        doc="Telegram chat id",
    )
    url = Column("url", TEXT, nullable=True, doc="Telegram url")
    username = Column("username", TEXT, nullable=True, doc="Telegram username")
    full_name = Column("full_name", TEXT, nullable=True, doc="Full name")
    role = Column(
        "role",
        TEXT,
        nullable=False,
        default="user",
        doc="User role from list [user, admin]",
    )
    team_id = Column(UUID(as_uuid=True), nullable=True)

    def __repr__(self) -> str:
        return (
            f"chat_id: {self.chat_id}\n"
            f"username: @{self.username}\n"
            f"full_name: {self.full_name}\n"
            f"role: {self.role}\n"
            f"team_id: {self.team_id}\n"
        )

    @property
    def line_info(self):
        return f"{self.full_name}, @{self.username}, {self.url}, {self.chat_id}"

    @classmethod
    def get(cls, db: Session, **kwargs):
        db_user: cls = db.query(cls).filter_by(**kwargs).first()
        return db_user

    @classmethod
    def get_all(cls, db: Session, **kwargs):
        db_user: cls = db.query(cls).filter_by(**kwargs).all()
        return db_user if db_user is not None else []
