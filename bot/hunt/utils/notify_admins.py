from aiogram.types import ParseMode
from sqlalchemy.orm import Session

from hunt import BotHolder
from hunt.db import get_db
from hunt.db.models import User


async def notify_admins(db: Session, text: str):
    bot = BotHolder().bot
    users: list[User] = User.get_all(db, role="admin")
    for user in users:
        try:
            await bot.send_message(user.chat_id, text, parse_mode=ParseMode.HTML)
        except:
            pass
