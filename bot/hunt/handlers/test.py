import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.db.models import Team, User, Task
from hunt.utils import admin_method, user_exists


def register_handlers_test(dp: Dispatcher):
    dp.register_message_handler(
        clear_user, commands="clear_clear_clear_user", state="*"
    )
    dp.register_message_handler(
        clear_team, commands="clear_clear_clear_team", state="*"
    )
    dp.register_message_handler(
        test, commands="test_test_test", state="*"
    )


@user_exists
@admin_method
async def clear_user(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        users = db.query(User).all()
        users = users if users is not None else []
        for user in users:
            db.delete(user)
        db.commit()
    await message.answer("Cleared")


@user_exists
@admin_method
async def clear_team(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        teams = db.query(Team).all()
        teams = teams if teams is not None else []
        for team in teams:
            db.delete(team)
        db.commit()
    await message.answer("Cleared")


@user_exists
@admin_method
async def test(message: Message, state: FSMContext):
    flags = ['DOMINICK_PRECARIOUS_VAMPIRE', 'MEDIATE_AUGER_ROTARIAN', 'CARDBOARD_EMULATE_DEANNA', 'THUBAN_LINDA_PAULINE', 'ELAN_RELISH_CAKE', 'FLEEING_TOLERANT_MAGAZINE', 'TRANSFORM_HOMAGE_GARRETT', 'CARTOON_NEFARIOUS_EPISCOPALIAN']
    type = 'secret'

    with get_db() as db:
        for i, flag in enumerate(flags):
            task = Task(name="Special Secret " + str(i), description="Special Secret...", type=type, image=None, flag=flag, amount=300)
            db.add(task)
        db.commit()


