from aiogram.types import ParseMode
from sqlalchemy.orm import Session

from hunt import BotHolder
from hunt.db import get_db
from hunt.db.models import User
from hunt.utils import kb_from_state


async def notify_team(db: Session, chat_id: int, text: str):
    bot = BotHolder().bot
    db_user: User = User.get(db, chat_id=chat_id)
    users: list[User] = User.get_all(db, team_id=db_user.team_id)
    for user in users:
        try:
            await bot.send_message(user.chat_id, text, parse_mode=ParseMode.HTML)
        except:
            pass


async def notify_team_by_id(db: Session, team_id: int, text: str):
    bot = BotHolder().bot
    users: list[User] = User.get_all(db, team_id=team_id)
    for user in users:
        try:
            await bot.send_message(user.chat_id, text, parse_mode=ParseMode.HTML)
        except:
            pass
