from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from hunt import BotHolder
from hunt.db import get_db
from hunt.db.models import User


def admin_method(func):
    async def wrapper(message: Message, state: FSMContext):
        with get_db() as db:
            bot = BotHolder().bot
            db_user: User = db.query(User).where(User.chat_id == message.chat.id).first()
            exists = db_user is not None
            if not exists:
                return
            if db_user.role != "admin":
                return
            db.close()

        return await func(message, state)

    return wrapper
