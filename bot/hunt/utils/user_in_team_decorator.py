from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.db.models import User
from hunt.utils import send_answer


def user_in_team(func):
    async def wrapper(message: Message, state: FSMContext):
        with get_db() as db:
            db_user: User = db.query(User).where(User.chat_id == message.chat.id).first()
            exists = db_user is not None
            if not exists:
                return await send_answer(db, message.chat.id, "no_team_action")
            if db_user.team_id is None:
                return await send_answer(db, message.chat.id, "no_team_action")

        return await func(message, state)

    return wrapper
