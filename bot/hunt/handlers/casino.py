import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ParseMode, CallbackQuery
from sqlalchemy.orm import Session

from hunt.utils import send_answer, user_exists, user_in_team, notify_team
from hunt import BotHolder
from datetime import datetime, timedelta
from hunt.replies import replies
from hunt.keyboard import casino_bet_amount, casino_bet_option, casino_wait, close_kb
from hunt.services import TeamManager
from hunt.db.models import Team, User
from hunt.db import get_db


opts = ['red', 'black', 'green']
weights = [5, 5, 1]
rates = {
    'red': 2,
    'black': 2,
    'green': 10,
}


def register_handlers_casino(dp: Dispatcher):
    dp.register_message_handler(casino_start, commands="casino", state="*")
    dp.register_message_handler(casino_start, Text(startswith="casino ", ignore_case=True), state="*")
    dp.register_message_handler(casino_start, Text(endswith="casino", ignore_case=True), state="*")
    dp.register_message_handler(casino_start, Text(equals="casino", ignore_case=True), state="*")
    dp.register_callback_query_handler(make_bet, Text(startswith="bet_amount_"), state=CasinoStates.choosing_amount)
    dp.register_callback_query_handler(choose_option, Text(startswith="bet_option_"), state=CasinoStates.choosing_option)


class CasinoStates(StatesGroup):
    choosing_amount = State()
    choosing_option = State()


@user_exists
@user_in_team
async def casino_start(message: Message, state: FSMContext):
    await message.answer(replies["casino_start"], parse_mode=ParseMode.HTML, reply_markup=casino_bet_amount)
    await CasinoStates.choosing_amount.set()


async def make_bet(query: CallbackQuery, state: FSMContext):
    amount = int(query.data.split("_")[-1])
    with get_db() as db:
        team: Team = TeamManager().team(db, query.message.chat.id)
    if team is None:
        return await query.answer("You are not in team!")
    if team.amount < amount:
        return await query.answer(f"You don't have enough points! (balance: {team.amount})")

    await state.update_data(bet_amount=amount)
    await CasinoStates.choosing_option.set()
    await query.message.edit_text(f"<b>Your bet: {amount} points</b>\n\n" + replies["casino_choose_option"],
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=casino_bet_option)


async def choose_option(query: CallbackQuery, state: FSMContext):
    option = query.data.split("_")[-1]
    amount = (await state.get_data()).get("bet_amount", 10)
    with get_db() as db:
        user: User = User.get(db, chat_id=query.message.chat.id)
        team: Team = Team.get(db, id=user.team_id)
        if team is None:
            return await query.answer("You are not in team!")
        if team.amount < amount:
            return await query.answer(f"You don't have enough points! (balance: {team.amount})")

        team.amount -= amount
        db.commit()
    await state.update_data(option=option)
    await query.message.edit_text(f"<b>10 seconds left...</b>\n"
                                  f"<b>Your bet: {amount} points</b>\n"
                                  f"<b>Chosen option: {option.upper()}</b>\n\n" + replies["casino_wait"],
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=casino_wait)
    args = [query, state, 10]
    BotHolder().scheduler.add_job(casino_tick, args=args, trigger='date', next_run_time=datetime.now() + timedelta(seconds=1))


async def casino_tick(query: CallbackQuery, state: FSMContext, time_left: int):
    time_left -= 1
    option = (await state.get_data()).get("option", "red")
    amount = (await state.get_data()).get("bet_amount", 10)
    if time_left <= 0:
        result = random.choices(opts, weights=weights)[0]
        with get_db() as db:
            user: User = User.get(db, chat_id=query.message.chat.id)
            team: Team = Team.get(db, id=user.team_id)
            if team is None:
                await state.finish()
                return await query.answer("You are not in team!")
            if result == option:
                new_text = f"Result: {result.upper()}\nWOW!! You win and earned {(rates[result] - 1) * amount}!"
                await query.message.edit_text(new_text, parse_mode=ParseMode.HTML, reply_markup=close_kb)
                await notify_team(db, query.message.chat.id, f"WTF?! You just earned {(rates[result] - 1) * amount} points in casino!")
                team.amount += rates[result] * amount
                db.commit()
            else:
                new_text = f"Result: {result.upper()}\nHE-HE!! You lose and lost {amount}!"
                await query.message.edit_text(new_text, parse_mode=ParseMode.HTML, reply_markup=close_kb)
                await notify_team(db, query.message.chat.id,
                                  f"LOL! You just LOST {amount} points in casino!")
        await state.finish()
    else:
        await query.message.edit_text(f"<b>{time_left} seconds left...</b>\n"
                                      f"<b>Your bet: {amount} points</b>\n"
                                      f"<b>Chosen option: {option.upper()}</b>\n\n" + replies["casino_wait"],
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=casino_wait)
        BotHolder().scheduler.add_job(casino_tick, args=[query, state, time_left], trigger='date', next_run_time=datetime.now() + timedelta(seconds=1))

