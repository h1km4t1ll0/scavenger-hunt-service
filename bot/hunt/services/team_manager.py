from enum import Enum
from uuid import UUID

from singleton_decorator import singleton
from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.db.models import Team, User
from hunt.utils.random_token import random_token
from hunt.utils.notify_admins import notify_admins
from hunt.utils.notify_team import notify_team_by_id


class TeamOperationResult(Enum):
    NAME_TAKEN = 0
    ALREADY_IN_TEAM = 1
    JOINED = 2
    CREATED = 3
    FULL_TEAM = 4
    INVALID_TOKEN = 5
    NOT_IN_TEAM = 6
    LEFT = 7


@singleton
class TeamManager:
    @staticmethod
    async def create_team(db: Session, chat_id: int, name: str) -> (TeamOperationResult, str):
        db_team: Team = db.query(Team).where(Team.name == name).first()
        print(name)
        if db_team is not None:
            return TeamOperationResult.NAME_TAKEN, None
        # if TeamManager().check_user_in_team(db, chat_id):
        #     return TeamOperationResult.ALREADY_IN_TEAM, None

        token = random_token(4)
        new_team: Team = Team(name=name, token=token)
        db.add(new_team)
        db.commit()
        # db.refresh(new_team)
        # db_user: User = User.get(db, chat_id=chat_id)
        # db_user.team_id = new_team.id
        # new_team.member_number += 1
        # db.commit()

        await notify_admins(db, f"New team {new_team.name} was created")

        return TeamOperationResult.CREATED, new_team.token

    @staticmethod
    def team_id(db: Session, chat_id) -> UUID:
        user: User = User.get(db, chat_id=chat_id)
        return user.team_id

    @staticmethod
    def team(db: Session, chat_id) -> Team:
        user: User = User.get(db, chat_id=chat_id)
        team: Team = Team.get(db, id=user.team_id)
        return team

    @staticmethod
    def check_user_in_team(db: Session, chat_id) -> bool:
        user: User = User.get(db, chat_id=chat_id)
        return user.team_id is not None

    @staticmethod
    async def join_team(db: Session, chat_id: int, token: str) -> TeamOperationResult:
        if TeamManager().check_user_in_team(db, chat_id):
            return TeamOperationResult.ALREADY_IN_TEAM

        user: User = User.get(db, chat_id=chat_id)
        team: Team = Team.get(db, token=token)
        if team is None:
            return TeamOperationResult.INVALID_TOKEN

        await notify_team_by_id(db, team.id, f"@{user.username} joined your team")

        user.team_id = team.id
        team.member_number += 1
        db.commit()

        return TeamOperationResult.JOINED

    @staticmethod
    async def leave_team(db: Session, chat_id: int) -> TeamOperationResult:
        if not TeamManager().check_user_in_team(db, chat_id):
            return TeamOperationResult.NOT_IN_TEAM

        user: User = User.get(db, chat_id=chat_id)
        team: Team = Team.get(db, id=user.team_id)
        user.team_id = None
        team.member_number -= 1
        db.commit()
        await notify_team_by_id(db, team.id, f"@{user.username} left your team")
        return TeamOperationResult.LEFT
