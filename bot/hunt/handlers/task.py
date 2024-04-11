from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, InputFile, Message, ParseMode

from hunt import BotHolder
from hunt.handlers.quiz import quiz_info, quiz_info_from_btn
from hunt.replies import replies
from hunt.config import get_settings
from hunt.db.connection.session import get_db
from hunt.db.models import Team, User, Task
from hunt.keyboard import (
    back_kb,
    close_kb,
    cosplay_tasks_kb,
    default_tasks_markup,
    offline_tasks_kb,
    online_tasks_kb,
    secrets_tasks_kb,
    songs_tasks_kb,
    rhymes_tasks_kb,
    manager_close_kb, manager_back_kb, manager_check_kb,
)
from hunt.services import TaskActionResult, TaskManager, TeamManager
from hunt.utils import notify_team, send_answer, user_exists, user_in_team


def register_handlers_task(dp: Dispatcher):
    # Tasks
    dp.register_message_handler(get_task_type_message, commands="tasks", state="*")
    dp.register_message_handler(
        get_task_type_message, Text(startswith="tasks ", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        get_task_type_message, Text(endswith=" tasks", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        get_task_type_message, Text(equals="tasks", ignore_case=True), state="*"
    )

    # Button handlers (buttons initialized in inline_keyboard.py
    dp.register_callback_query_handler(
        online_tasks_message, Text(equals="online_tasks_btn"), state="*"
    )
    dp.register_callback_query_handler(
        offline_tasks_message, Text(equals="offline_tasks_btn"), state="*"
    )
    dp.register_callback_query_handler(
        cosplay_tasks_message, Text(equals="cosplay_btn"), state="*"
    )
    dp.register_callback_query_handler(
        secrets_tasks_message, Text(equals="secrets_btn"), state="*"
    )
    dp.register_callback_query_handler(
        songs_tasks_message, Text(equals="songs_btn"), state="*"
    )
    dp.register_callback_query_handler(
        rhymes_tasks_message, Text(equals="rhymes_btn"), state="*"
    )
    dp.register_callback_query_handler(
        quiz_info_from_btn, Text(equals="quiz_btn"), state="*"
    )

    # Task list display handlers
    dp.register_callback_query_handler(
        display_task, Text(startswith="cosplay_task_"), state="*"
    )
    dp.register_callback_query_handler(
        display_task, Text(startswith="offline_task_"), state="*"
    )
    dp.register_callback_query_handler(
        display_task, Text(startswith="online_task_"), state="*"
    )
    dp.register_callback_query_handler(
        display_task, Text(startswith="song_task_"), state="*"
    )
    dp.register_callback_query_handler(
        display_task, Text(startswith="rhyme_task_"), state="*"
    )

    # System handlers
    dp.register_callback_query_handler(back, Text(startswith="back_"), state="*")
    dp.register_callback_query_handler(close, Text(equals="close"), state="*")
    dp.register_callback_query_handler(send_map, Text(equals="map"), state="*")

    dp.register_message_handler(flag_start, commands="flag", state="*")
    dp.register_message_handler(
        flag_start, Text(startswith="flag ", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        flag_start, Text(endswith=" flag", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        flag_start, Text(equals="flag", ignore_case=True), state="*"
    )

    dp.register_message_handler(flag_flag, state=FlagStates.waiting_flag)

    dp.register_callback_query_handler(solve_task_start, Text(startswith="solve_task_"), state="*")
    dp.register_message_handler(solve_task_read_message, content_types=["any"], state=SolveStates.waiting_message)


@user_exists
@user_in_team
async def get_task_type_message(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        replies["tasks_types"],
        parse_mode=ParseMode.HTML,
        reply_markup=default_tasks_markup,
    )


async def online_tasks_message(query: CallbackQuery, state: FSMContext):
    with get_db() as db:
        await query.message.edit_text(
            replies["online_tasks_description"], parse_mode=ParseMode.HTML,
            reply_markup=online_tasks_kb(db, TeamManager().team_id(db, query.message.chat.id))
        )
    db.close()


async def offline_tasks_message(query: CallbackQuery, state: FSMContext):
    with get_db() as db:
        await query.message.edit_text(
            replies["offline_tasks_description"], parse_mode=ParseMode.HTML,
            reply_markup=offline_tasks_kb(db, TeamManager().team_id(db, query.message.chat.id))
        )
    db.close()


async def cosplay_tasks_message(query: CallbackQuery, state: FSMContext):
    with get_db() as db:
        await query.message.edit_text(
            replies["cosplay_tasks_description"], parse_mode=ParseMode.HTML,
            reply_markup=cosplay_tasks_kb(db, TeamManager().team_id(db, query.message.chat.id))
        )
    db.close()


async def secrets_tasks_message(query: CallbackQuery, state: FSMContext):
    with get_db() as db:
        await query.message.edit_text(
            replies["secrets_tasks_description"], parse_mode=ParseMode.HTML,
            reply_markup=secrets_tasks_kb(db, TeamManager().team_id(db, query.message.chat.id))
        )
    db.close()


async def songs_tasks_message(query: CallbackQuery, state: FSMContext):
    with get_db() as db:
        await query.message.edit_text(
            replies["songs_tasks_description"], parse_mode=ParseMode.HTML,
            reply_markup=songs_tasks_kb(db, TeamManager().team_id(db, query.message.chat.id))
        )
    db.close()


async def rhymes_tasks_message(query: CallbackQuery, state: FSMContext):
    with get_db() as db:
        await query.message.edit_text(
            replies["rhymes_tasks_description"], parse_mode=ParseMode.HTML,
            reply_markup=rhymes_tasks_kb(db, TeamManager().team_id(db, query.message.chat.id))
        )
    db.close()


async def display_task(query: CallbackQuery, state: FSMContext):
    task_id = query.data.split("_")[-1]
    with get_db() as db:
        task = TaskManager().get_task(db, task_id)
        if task.usage <= 0:
            db.close()
            await query.message.edit_text("This task was solved too many times already...",
                                          reply_markup=back_kb(task.type))
            return
    new_text = f"❗ <b>{task.name}</b> ❗\n\n{task.description}\n<i>Maximum point(s): {task.amount}</i>"
    db.close()
    if task.image is not None:
        new_photo = InputFile(get_settings().SRC_PREFIX + task.image)
        if task.with_manager:
            new_kb = manager_close_kb(task.name)
        else:
            new_kb = close_kb
        await query.message.answer_photo(
            new_photo, caption=new_text, parse_mode=ParseMode.HTML, reply_markup=new_kb
        )
    else:
        if task.with_manager:
            new_kb = manager_back_kb(task.name, task.type)
        else:
            new_kb = back_kb(task.type)
        await query.message.edit_text(
            new_text, parse_mode=ParseMode.HTML, reply_markup=new_kb
        )


class SolveStates(StatesGroup):
    waiting_message = State()


async def solve_task_start(query: CallbackQuery, state: FSMContext):
    task_name = query.data.split("_")[-1]
    await state.update_data(task_name=task_name)
    with get_db() as db:
        await send_answer(db, query.message.chat.id, "solve_task_start")
    db.close()
    await SolveStates.waiting_message.set()


@user_in_team
async def solve_task_read_message(message: Message, state: FSMContext):
    with get_db() as db:
        task_name = (await state.get_data()).get("task_name", "empty")
        task: Task = db.query(Task).where(Task.name == task_name).first()
        if task is None:
            await state.finish()
            return await message.answer("Some troubles with task, use /support")
        if not task.with_manager:
            await state.finish()
            return await message.answer("This task has no manager")

        user: User = db.query(User).where(User.chat_id == message.chat.id).first()
        team: Team = db.query(Team).where(Team.id == user.team_id).first()
        solved = TaskManager().check_task_solved(db, task.id, team.id)
        if solved:
            manager_text = f"New solution!\n\nTask: {task.name}\nTeam: {team.name}\n" \
                           f"Comment: This team has already solved this task " \
                           f"(they have already somehow received some amount of points), check your history " \
                           f"and then make a decision (you can answer them, give points or do nothing)"
        else:
            manager_text = f"New solution!\n\nTask: {task.name}\nTeam: {team.name}"
        if task.manager_id is None:
            await state.finish()
            db.close()
            return await message.answer("This task has no manager, use /support")
        bot: Bot = BotHolder().bot
        try:
            await message.forward(task.manager_id)
            await bot.send_message(task.manager_id, manager_text, reply_markup=manager_check_kb(team.name, task.name))
            task.usage -= 1
            db.commit()
        except:
            db.close()
            return await message.answer("Some troubles while resending was acquired, use /support")
        finally:
            await state.finish()
            db.close()
        return await send_answer(db, message.chat.id, "solution_sent")


async def menu(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(replies["tasks_types"], parse_mode=ParseMode.HTML, reply_markup=default_tasks_markup)


async def back(query: CallbackQuery, state: FSMContext):
    path = query.data.split("_")[-1]
    if path == "tasks":
        await menu(query, state)
    elif path == "cosplay":
        await cosplay_tasks_message(query, state)
    elif path == "online":
        await online_tasks_message(query, state)
    elif path == "offline":
        await offline_tasks_message(query, state)
    elif path == "song summarization":
        await songs_tasks_message(query, state)
    elif path == "rhymes":
        await rhymes_tasks_message(query, state)


async def close(query: CallbackQuery, state: FSMContext):
    await query.message.delete()


class FlagStates(StatesGroup):
    waiting_flag = State()


@user_exists
@user_in_team
async def flag_start(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        await send_answer(db, message.chat.id, "send_flag")
    db.close()
    await FlagStates.waiting_flag.set()


async def flag_flag(message: Message, state: FSMContext):
    flag = message.text.upper()
    await state.finish()
    with get_db() as db:
        result, amount = await TaskManager().solve_task(db, flag, message.chat.id)
        if result == TaskActionResult.OK_FLAG:
            await notify_team(
                db, message.chat.id, f"Congrats! Your team just earned <b>{amount} point(s)!</b> 🤑"
            )
        elif result == TaskActionResult.INVALID_FLAG:
            await send_answer(db, message.chat.id, "invalid_flag")
        elif result == TaskActionResult.NEGATIVE_FLAG:
            await notify_team(
                db,
                message.chat.id,
                f"Oh... You team just <b>LOST {abs(amount)} point(s)!</b> 😓",
            )
        elif result == TaskActionResult.MAXIMUM_USAGE_EXCEEDED:
            await send_answer(db, message.chat.id, "task_usage_exceeded")
        elif result == TaskActionResult.USED_FLAG:
            await send_answer(db, message.chat.id, "used_flag")
    db.close()


async def send_map(query: CallbackQuery, state: FSMContext):
    await state.finish()
    with get_db() as db:
        await send_answer(db, query.message.chat.id, "map")
    db.close()
