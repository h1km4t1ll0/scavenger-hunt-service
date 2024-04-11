from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ParseMode
from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.db.models import Team, User
from hunt.services import TeamManager, TeamOperationResult
from hunt.utils import (
    admin_method,
    number_to_emoji,
    send_answer,
    user_exists,
    user_in_team,
)


def register_handlers_team(dp: Dispatcher):
    dp.register_message_handler(create_team_start, commands="create_team", state="*")
    dp.register_message_handler(
        create_team_read_name, state=CreateTeamStates.waiting_name
    )

    dp.register_message_handler(join_team_start, commands="join_team", state="*")
    dp.register_message_handler(
        join_team_start, Text(startswith="join team ", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        join_team_start, Text(endswith=" join team", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        join_team_start, Text(equals="join team", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        join_team_read_token, state=JoinTeamStates.waiting_token
    )

    dp.register_message_handler(leave_team, commands="leave_team", state="*")
    dp.register_message_handler(
        leave_team, Text(startswith="leave ", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        leave_team, Text(endswith=" leave", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        leave_team, Text(equals="leave", ignore_case=True), state="*"
    )
    dp.register_message_handler(team_info, commands="my_team", state="*")
    dp.register_message_handler(
        team_info, Text(startswith="my team ", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        team_info, Text(endswith=" my team", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        team_info, Text(equals="my team", ignore_case=True), state="*"
    )
    dp.register_message_handler(leaderboard, commands="scoreboard", state="*")
    dp.register_message_handler(
        leaderboard, Text(startswith="scoreboard ", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        leaderboard, Text(endswith=" scoreboard", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        leaderboard, Text(equals="scoreboard", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        leaderboard, Text(startswith="leaderboard", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        leaderboard, Text(endswith="leaderboard", ignore_case=True), state="*"
    )


class CreateTeamStates(StatesGroup):
    waiting_name = State()


@user_exists
@admin_method
async def create_team_start(message: Message, state: FSMContext):
    try:
        await state.finish()
        with get_db() as db:
            # if TeamManager().check_user_in_team(db, message.chat.id):
            #     return await send_answer(db, message.chat.id, "create_team_already_in_team")
            await send_answer(db, message.chat.id, "create_team_start")
        await CreateTeamStates.waiting_name.set()
        db.close()
    except Exception as e:
        print(e)
        db.close()


async def create_team_read_name(message: Message, state: FSMContext):
    try:
        name = message.text
        await state.finish()
        with get_db() as db:
            result, token = await TeamManager().create_team(db, message.chat.id, name)
            # if result == TeamOperationResult.ALREADY_IN_TEAM:
            #     return await send_answer(db, message.chat.id, "create_team_already_in_team")
            if result == TeamOperationResult.NAME_TAKEN:
                return await send_answer(db, message.chat.id, "create_team_name_is_taken")
            elif result == TeamOperationResult.CREATED:
                await send_answer(db, message.chat.id, "create_team_created")
                return await message.answer(
                    f"<span class='tg-spoiler'>{token}</span>", parse_mode=ParseMode.HTML
                )
            db.close()
    except Exception as e:
        print(e)
        db.close()


class JoinTeamStates(StatesGroup):
    waiting_token = State()


@user_exists
async def join_team_start(message: Message, state: FSMContext):
    try:
        await state.finish()
        with get_db() as db:
            if TeamManager().check_user_in_team(db, message.chat.id):
                return await send_answer(db, message.chat.id, "join_team_already_in_team")
            await send_answer(db, message.chat.id, "join_team_start")
            db.close()
        await JoinTeamStates.waiting_token.set()
    except Exception as e:
        print(e)
        db.close()


async def join_team_read_token(message: Message, state: FSMContext):
    try:
        token = message.text
        await state.finish()
        with get_db() as db:
            result = await TeamManager().join_team(db, message.chat.id, token)
            if result == TeamOperationResult.ALREADY_IN_TEAM:
                return await send_answer(db, message.chat.id, "join_team_already_in_team")
            elif result == TeamOperationResult.INVALID_TOKEN:
                return await send_answer(db, message.chat.id, "join_team_token_invalid")
            elif result == TeamOperationResult.FULL_TEAM:
                return await send_answer(db, message.chat.id, "join_team_full_team")
            elif result == TeamOperationResult.JOINED:
                return await send_answer(db, message.chat.id, "join_team_joined")
            db.close()
    except Exception as e:
        print(e)
        db.close()


@user_exists
async def leave_team(message: Message, state: FSMContext):
    try:
        await state.finish()
        with get_db() as db:
            result = await TeamManager().leave_team(db, message.chat.id)
            if result == TeamOperationResult.NOT_IN_TEAM:
                return await send_answer(db, message.chat.id, "leave_team_not_in_team")
            if result == TeamOperationResult.LEFT:
                return await send_answer(db, message.chat.id, "leave_team_left")
            db.close()
    except Exception as e:
        print(e)
        db.close()


@user_exists
@user_in_team
async def team_info(message: Message, state: FSMContext):
    try:
        await state.finish()
        with get_db() as db:
            team: Team = TeamManager().team(db, message.chat.id)
            users: list[User] = User.get_all(db, team_id=team.id)
            db.close()
        info = (
            f"❗ <b>{team.name}</b> ❗\n"
            f"💰 You have <i>{team.amount} points</i>\n\n"
            f"{team.member_number} hunters:\n"
        )
        for user in users:
            info += f"▪ {user.full_name} @{user.username}\n"
        await message.answer(info, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(e)
        db.close()


async def leaderboard(message: Message, state: FSMContext):
    try:
        await state.finish()
        with get_db() as db:
            teams: list[Team] = db.query(Team).all()
        db.close()
        teams = teams if teams is not None else []
        teams.sort()
        teams.reverse()

        board = f"<b><i>Scavenger Hunt scoreboard</i></b>\n\n"
        board += "<pre>"
        for team in teams:
            if team.visible:
                score = number_to_emoji(team.amount)
                board += f"{score}" + " | " + f"{team.name}\n"
        board += "</pre>"
        await message.answer(board, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(e)
        db.close()
