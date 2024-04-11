from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.db.models import User


def user_exists(func):
    async def wrapper(message: Message, state: FSMContext):
        with get_db() as db:
            db_user: User = db.query(User).where(User.chat_id == message.chat.id).first()
            exists = db_user is not None
            if not exists:
                db_user = User(
                    chat_id=message.chat.id,
                    username=message.from_user.username,
                    full_name=message.from_user.full_name,
                    url=message.from_user.url
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)

        return await func(message, state)

    return wrapper
