from enum import Enum
from uuid import UUID

from singleton_decorator import singleton
from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.db.models import SolvedTasks, Task, Team, User, Results
from hunt.utils.notify_admins import notify_admins


class TaskActionResult(Enum):
    INVALID_FLAG = 0
    OK_FLAG = 1
    NEGATIVE_FLAG = 2
    MAXIMUM_USAGE_EXCEEDED = 3
    USED_FLAG = 4


@singleton
class TaskManager:
    @staticmethod
    def get_online_tasks(db: Session, ):
        tasks = Task().get_all(db, type="online")
        return tasks if tasks is not None else []

    @staticmethod
    def get_offline_tasks(db: Session, ):
        tasks = Task().get_all(db, type="offline")
        return tasks if tasks is not None else []

    @staticmethod
    def get_cosplay_tasks(db: Session, ):
        tasks = Task().get_all(db, type="cosplay")
        return tasks if tasks is not None else []

    @staticmethod
    def get_secrets_tasks(db: Session, ):
        tasks = Task().get_all(db, type="secret")
        return tasks if tasks is not None else []

    @staticmethod
    def get_songs_tasks(db: Session, ):
        tasks = Task().get_all(db, type="song summarization")
        return tasks if tasks is not None else []

    @staticmethod
    def get_rhymes_tasks(db: Session, ):
        tasks = Task().get_all(db, type="rhymes")
        return tasks if tasks is not None else []

    @staticmethod
    def count_solved_tasks(db: Session, tasks: list, team_id: UUID) -> (int, int):
        solved_number = 0
        tasks_number = len(tasks)
        for task in tasks:
            solved: SolvedTasks = (
                db.query(SolvedTasks)
                .filter_by(task_id=task.id, team_id=team_id)
                .first()
            )
            if solved is not None:
                solved_number += 1

        return solved_number, tasks_number

    @staticmethod
    def check_task_solved(db: Session, task_id: UUID, team_id: UUID) -> bool:
        solved: SolvedTasks = (
            db.query(SolvedTasks).filter_by(task_id=task_id, team_id=team_id).first()
        )
        if solved is not None:
            return True
        return False

    @staticmethod
    def get_task(db: Session, task_id: str) -> Task:
        task: Task = db.query(Task).where(Task.id == task_id).first()
        return task

    @staticmethod
    async def solve_task(db: Session, flag: str, chat_id: str) -> (TaskActionResult, int):
        task: Task = db.query(Task).where(Task.flag == flag).first()
        if task is None:
            return TaskActionResult.INVALID_FLAG, 0
        if task.usage <= 0:
            return TaskActionResult.MAXIMUM_USAGE_EXCEEDED, 0

        user: User = User.get(db, chat_id=chat_id)
        team: Team = Team.get(db, id=user.team_id)

        if TaskManager().check_task_solved(db, task.id, team.id):
            return TaskActionResult.USED_FLAG, 0

        Results.write(db, team.id, task.id, task.amount)
        team.amount += task.amount
        task.usage -= 1
        solved_task: SolvedTasks = SolvedTasks(task_id=task.id, team_id=team.id)
        db.add(solved_task)
        db.commit()

        # await notify_admins(db, f"Team {team.name} solved task {task.name}")

        if task.amount < 0:
            return TaskActionResult.NEGATIVE_FLAG, abs(task.amount)
        return TaskActionResult.OK_FLAG, task.amount
