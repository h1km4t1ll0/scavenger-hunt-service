import asyncio
import random
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    InputFile,
    KeyboardButton,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, CallbackQuery,
)
from aiogram.utils.markdown import hspoiler, hbold
from sqlalchemy.orm import Session

from hunt import BotHolder
from hunt.config import get_settings
from hunt.db import get_db
from hunt.db.models import Task, Team, User, Results, SolvedTasks
from hunt.keyboard import manager_checked_kb, manager_check_kb
from hunt.utils import admin_method, notify_team_by_id, user_exists, notify_admins, build_results


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands="admin", state="*")
    dp.register_message_handler(admin_token, state=AdminRegisterStates.waiting_token)

    dp.register_message_handler(get_tasks, commands="get_tasks", state="*")
    dp.register_message_handler(get_teams, commands="get_teams", state="*")

    dp.register_message_handler(give_money_start, commands="give_points", state="*")
    dp.register_message_handler(give_money_read_team, state=GiveMoneyState.waiting_team)
    dp.register_message_handler(give_money_read_task, state=GiveMoneyState.waiting_task)
    dp.register_message_handler(
        give_money_read_amount, state=GiveMoneyState.waiting_amount
    )

    dp.register_message_handler(remove_task_start, commands="remove_task", state="*")
    dp.register_message_handler(remove_task, state=RemoveTaskStates.waiting_name)

    dp.register_message_handler(add_task_start, commands="add_task", state="*")
    dp.register_message_handler(read_task_type, state=AddTaskStates.waiting_type)
    dp.register_message_handler(read_task_name, state=AddTaskStates.waiting_name)
    dp.register_message_handler(
        read_task_description, state=AddTaskStates.waiting_description
    )
    dp.register_message_handler(
        read_task_image, content_types=["photo"], state=AddTaskStates.waiting_image
    )
    dp.register_message_handler(
        read_task_image_empty, state=AddTaskStates.waiting_image
    )
    dp.register_message_handler(read_task_flag, state=AddTaskStates.waiting_flag)
    dp.register_message_handler(read_task_amount, state=AddTaskStates.waiting_amount)
    dp.register_message_handler(read_task_usage, state=AddTaskStates.waiting_usage)
    dp.register_message_handler(read_task_with_manager, state=AddTaskStates.waiting_with_manager)
    dp.register_message_handler(read_task_end, state=AddTaskStates.waiting_confirm)

    dp.register_message_handler(get_users, commands="get_users", state="*")

    dp.register_message_handler(mailing_all_start, commands="mailing_all", state="*")
    dp.register_message_handler(
        mailing_all_read_text, state=MailingAllStates.waiting_text
    )
    dp.register_message_handler(
        mailing_all_read_image,
        content_types="photo",
        state=MailingAllStates.waiting_image,
    )
    dp.register_message_handler(
        mailing_all_read_image_none,
        content_types="text",
        state=MailingAllStates.waiting_image,
    )
    dp.register_message_handler(
        mailing_all_confirm, state=MailingAllStates.waiting_confirm
    )

    dp.register_message_handler(mailing_team_start, commands="mailing_team", state="*")
    dp.register_message_handler(
        mailing_team_read_team_name, state=MailingTeamStates.waiting_team_name
    )
    dp.register_message_handler(
        mailing_team_read_text, state=MailingTeamStates.waiting_text
    )
    dp.register_message_handler(
        mailing_team_confirm, state=MailingTeamStates.waiting_confirm
    )

    dp.register_message_handler(change_visibility_start, commands="change_visibility", state="*")
    dp.register_message_handler(change_visibility_read_team, state=ChangeVisibleStates.waiting_team_name)

    dp.register_message_handler(manager_start, commands="manager", state="*")
    dp.register_message_handler(manager_read_task, state=ManagerStates.waiting_task_name)

    dp.register_callback_query_handler(
        give_money_from_solution_callback, Text(startswith="solution_check_yes_"), state="*"
    )
    dp.register_callback_query_handler(
        mailing_team_from_solution_callback, Text(startswith="solution_check_send_"), state="*"
    )
    dp.register_callback_query_handler(
        solution_mark_checked, Text(startswith="solution_check_checked_"), state="*"
    )
    dp.register_callback_query_handler(
        solution_mark_unchecked, Text(startswith="solution_check_unchecked_"), state="*"
    )

    dp.register_message_handler(get_invite_tokens, commands="invite_tokens", state="*")
    dp.register_message_handler(build_results_start, commands="build_results", state="*")


class AdminRegisterStates(StatesGroup):
    waiting_token = State()


@user_exists
async def admin_start(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        db_user = db.query(User).where(User.chat_id == message.chat.id).first()
        if db_user.role == "admin":
            return await message.answer("Ты уже админ")
    await message.answer("Укажи токен авторизации админов")
    await AdminRegisterStates.waiting_token.set()


async def admin_token(message: Message, state: FSMContext):
    token = message.text
    settings = get_settings()
    with get_db() as db:
        db_user = db.query(User).where(User.chat_id == message.chat.id).first()
        if token != settings.ADMIN_TOKEN:
            return await message.answer("Токен - инвалид!")
        db_user.role = "admin"
        db.commit()
    db.close()
    await message.answer("Теперь ты админ")
    await state.finish()


class AddTaskStates(StatesGroup):
    waiting_type = State()
    waiting_name = State()
    waiting_description = State()
    waiting_image = State()
    waiting_flag = State()
    waiting_amount = State()
    waiting_usage = State()
    waiting_with_manager = State()
    waiting_confirm = State()


@user_exists
@admin_method
async def add_task_start(message: Message, state: FSMContext):
    await state.finish()
    kb = (
        ReplyKeyboardMarkup(resize_keyboard=True)
        .add(KeyboardButton("offline"))
        .add(KeyboardButton("online"))
        .add(KeyboardButton("cosplay"))
        .add(KeyboardButton("secret"))
        .add(KeyboardButton("song summarization"))
        .add(KeyboardButton("rhymes"))
    )
    await message.answer("Выбери тип таски", reply_markup=kb)
    await AddTaskStates.waiting_type.set()


async def read_task_type(message: Message, state: FSMContext):
    type = message.text
    await state.update_data(type=type)
    await message.answer("Введи имя таски")
    await AddTaskStates.waiting_name.set()


async def read_task_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Введи описание таски (ParseMode.HTML)")
    await AddTaskStates.waiting_description.set()


async def read_task_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer(
        "Дай мне фотку для описания таски (если ее нет - отправь любое текстовое сообщение)"
    )
    await AddTaskStates.waiting_image.set()


async def read_task_image(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    bot = BotHolder().bot
    image_info = await bot.get_file(image_id)
    downloaded_image = await bot.download_file(image_info.file_path)
    name = (await state.get_data()).get("name", str(random.randint(0, 100000)))
    with open(get_settings().SRC_PREFIX + name + ".png", "wb") as local_image:
        local_image.write(downloaded_image.getvalue())
    await state.update_data(image=(name + ".png"))
    await message.answer("Укажи флаг к таске")
    await AddTaskStates.waiting_flag.set()


async def read_task_image_empty(message: Message, state: FSMContext):
    await message.answer("Укажи флаг к таске")
    await AddTaskStates.waiting_flag.set()


async def read_task_flag(message: Message, state: FSMContext):
    flag = message.text
    await state.update_data(flag=flag)
    await message.answer("Укажи кол-во поинтов за таску")
    await AddTaskStates.waiting_amount.set()


async def read_task_amount(message: Message, state: FSMContext):
    amount = int(message.text)
    await state.update_data(amount=amount)
    await message.answer("Сколько команд может решить эту таску?")
    await AddTaskStates.waiting_usage.set()


async def read_task_usage(message: Message, state: FSMContext):
    usage = int(message.text)
    await state.update_data(usage=usage)
    await message.answer("Таска будет проверяться менеджером? (0 или 1)")
    await message.answer(str(await state.get_data()))
    await AddTaskStates.waiting_with_manager.set()


async def read_task_with_manager(message: Message, state: FSMContext):
    with_manager = bool(int(message.text))
    await state.update_data(with_manager=with_manager)
    await message.answer("Проверь таску (да/нет)")
    await message.answer(str(await state.get_data()))
    await AddTaskStates.waiting_confirm.set()


async def read_task_end(message: Message, state: FSMContext):
    confirm = message.text.lower()
    if "да" == confirm:
        new_task = Task(**(await state.get_data()))
        with get_db() as db:
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
        await message.answer(f"Таска {new_task.name} добавлена")
        await state.finish()
    elif "нет" == confirm:
        await message.answer("Действие отменено")
        await state.finish()
    else:
        await message.answer("Чё?")


class RemoveTaskStates(StatesGroup):
    waiting_name = State()


@user_exists
@admin_method
async def remove_task_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Введи имя таски на удаление")
    await RemoveTaskStates.waiting_name.set()


async def remove_task(message: Message, state: FSMContext):
    name = message.text
    with get_db() as db:
        db_task = db.query(Task).where(Task.name == name).first()
        exists = db_task is not None
        if not exists:
            await state.finish()
            return await message.answer("Таски с таким именем нет")

        db.delete(db_task)
        db.commit()
    db.close()
    await state.finish()
    await message.answer(f"Таска {name} удалена")


@user_exists
@admin_method
async def get_tasks(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        db_tasks: [Task] = db.query(Task).all()
    db.close()
    bot: Bot = BotHolder().bot
    for task in db_tasks:
        ans = f"Имя: {task.name}\nОписание:\n{task.description}\nЦена: {task.amount}\nФлаг: {task.flag}\nКол-во использований: {task.usage}"
        await message.answer(ans, parse_mode=ParseMode.HTML)
        if task.image is not None:
            photo = InputFile(get_settings().SRC_PREFIX + task.image)
            await bot.send_photo(message.chat.id, photo)


@user_exists
@admin_method
async def get_teams(message: Message, state: FSMContext):
    with get_db() as db:
        teams: list[Team] = db.query(Team).all()
        teams = teams if teams is not None else []
        text = f""
        for team in teams:
            text += f"{team.name} | {team.amount} points\n"
            users: list[User] = db.query(User).where(User.team_id == team.id).all()
            users = users if users is not None else []
            for user in users:
                text += f"@{user.username} "
            text += "\n\n"
    db.close()
    await message.answer(text)


class GiveMoneyState(StatesGroup):
    waiting_team = State()
    waiting_amount = State()
    waiting_task = State()


@user_exists
@admin_method
async def give_money_start(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        teams: list[Team] = db.query(Team).all()
    teams = teams if teams is not None else []
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for team in teams:
        kb.add(KeyboardButton(team.name))
    db.close()
    await message.answer("Choose team to give money", reply_markup=kb)
    await GiveMoneyState.waiting_team.set()


async def give_money_read_team(message: Message, state: FSMContext):
    team_name = message.text
    await state.update_data(team_name=team_name)

    with get_db() as db:
        tasks: list[Task] = db.query(Task).all()
    tasks = tasks if tasks is not None else []
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for task in tasks:
        kb.add(KeyboardButton(task.name))

    db.close()
    await message.answer(
        "Choose task", reply_markup=kb
    )
    await GiveMoneyState.waiting_task.set()


async def give_money_read_task(message: Message, state: FSMContext):
    task_name = message.text
    await state.update_data(task_name=task_name)
    await message.answer("Enter amount (might be negative)")
    await GiveMoneyState.waiting_amount.set()


async def give_money_from_solution_callback(query: CallbackQuery, state: FSMContext):
    team_name = query.data.split("_")[-2]
    task_name = query.data.split("_")[-1]
    await state.update_data(team_name=team_name, task_name=task_name)
    # await query.answer("Enter amount (might be negative)")
    await query.message.answer("Enter amount (might be negative)")
    await state.update_data(solution_message_id=query.message.message_id)
    await state.update_data(solution_message_text=query.message.text)
    await GiveMoneyState.waiting_amount.set()


async def give_money_read_amount(message: Message, state: FSMContext):
    amount = int(message.text)
    with get_db() as db:
        team_name = (await state.get_data())["team_name"]
        team: Team = db.query(Team).where(Team.name == team_name).first()
        if team is None:
            await state.finish()
            return await message.answer("No such team")

        task_name = (await state.get_data())["task_name"]
        task: Task = db.query(Task).where(Task.name == task_name).first()
        if task is None:
            await state.finish()
            return await message.answer("No such task")

        Results.write(db, team.id, task.id, amount)
        try:
            solved_task: SolvedTasks = SolvedTasks(team_id=team.id, task_id=task.id)
            db.add(solved_task)
            db.commit()
        except:
            pass
        team.amount += amount
        db.commit()
        if amount < 0:
            await notify_team_by_id(
                db, team.id, f"Oh... Your team just <b>LOST {abs(amount)} points</b> for the task <i>{task.name}</i>  😓"
            )
        else:
            await notify_team_by_id(
                db, team.id, f"Congrats! Your team just earned <b>{amount} points</b> for the task <i>{task.name}</i> 🤑"
            )

    data = (await state.get_data())
    solution_message_id = data.get("solution_message_id", None)
    solution_message_text = data.get("solution_message_text", None)
    team_name = data.get("team_name", None)
    task_name = data.get("task_name", None)
    if solution_message_id is not None and team_name is not None and task_name is not None and solution_message_text is not None:
        bot: Bot = BotHolder().bot
        await bot.edit_message_text(f"{solution_message_text}\nGiven: {amount}", message.chat.id, solution_message_id)
        await bot.edit_message_reply_markup(message.chat.id, solution_message_id,
                                            reply_markup=manager_checked_kb(team_name, task_name))
    db.close()
    await message.answer(f"{amount} points was given to {team_name}")
    await state.finish()


class ChangeVisibleStates(StatesGroup):
    waiting_team_name = State()


@user_exists
@admin_method
async def change_visibility_start(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        teams: list[Team] = db.query(Team).all()
    teams = teams if teams is not None else []
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for team in teams:
        kb.add(KeyboardButton(team.name))
    db.close()
    await message.answer("Choose team to change visibility", reply_markup=kb)
    await ChangeVisibleStates.waiting_team_name.set()


async def change_visibility_read_team(message: Message, state: FSMContext):
    with get_db() as db:
        team: Team = db.query(Team).where(Team.name == message.text).first()
        if team is None:
            await state.finish()
            return await message.answer("No such team")
        if team.visible:
            team.visible = False
        else:
            team.visible = True
        db.commit()
    db.close()
    await state.finish()
    await message.answer("Changed")


class MailingAllStates(StatesGroup):
    waiting_text = State()
    waiting_image = State()
    waiting_confirm = State()


@user_exists
@admin_method
async def mailing_all_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Write text to send (ParseMode.HTML)")
    await MailingAllStates.waiting_text.set()


async def mailing_all_read_text(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(
        "Send me photo (or text if you dont want to make mailing with photo)"
    )
    await MailingAllStates.waiting_image.set()


async def mailing_all_read_image_none(message: Message, state: FSMContext):
    await state.update_data(image=None)
    kb = ReplyKeyboardMarkup().add(KeyboardButton("yes")).add(KeyboardButton("no"))
    await message.answer("Type yes/no to confirm/decline mailing", reply_markup=kb)
    await MailingAllStates.waiting_confirm.set()


async def mailing_all_read_image(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    bot = BotHolder().bot
    image_info = await bot.get_file(image_id)
    downloaded_image = await bot.download_file(image_info.file_path)
    name = str(random.randint(0, 100000))
    with open(get_settings().SRC_PREFIX + name + ".png", "wb") as local_image:
        local_image.write(downloaded_image.getvalue())
    await state.update_data(image=(name + ".png"))

    kb = ReplyKeyboardMarkup().add(KeyboardButton("yes")).add(KeyboardButton("no"))
    await message.answer("Type yes/no to confirm/decline mailing", reply_markup=kb)
    await MailingAllStates.waiting_confirm.set()


async def mailing_all_confirm(message: Message, state: FSMContext):
    if message.text == "yes":
        with get_db() as db:
            users: list[User] = db.query(User).all()
        bot = BotHolder().bot
        text = (await state.get_data()).get("text", "Empty text")
        image_name = (await state.get_data()).get("image", "test.png")
        users = users if users is not None else []
        i = 0
        for user in users:
            # print("try")
            await asyncio.sleep(0.04)
            i += 1
            if image_name is not None:
                try:
                    await bot.send_photo(
                        user.chat_id,
                        InputFile(get_settings().SRC_PREFIX + image_name),
                        caption=text,
                        parse_mode=ParseMode.HTML,
                    )
                    print(f"{i} | {user.username} | {user.full_name}")
                except Exception as e:
                    print(e)
            else:
                try:
                    await bot.send_message(user.chat_id, text, parse_mode=ParseMode.HTML)
                    print(f"{i} | {user.username} | {user.full_name}")
                except:
                    pass
        db.close()
        await message.answer("Completed", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Canceled", reply_markup=ReplyKeyboardRemove())
    await state.finish()


class MailingTeamStates(StatesGroup):
    waiting_team_name = State()
    waiting_text = State()
    waiting_confirm = State()


@user_exists
@admin_method
async def mailing_team_start(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        teams: list[Team] = db.query(Team).all()
    teams = teams if teams is not None else []
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for team in teams:
        kb.add(KeyboardButton(team.name))
    db.close()
    await message.answer("Choose team to send message", reply_markup=kb)
    await MailingTeamStates.waiting_team_name.set()


async def mailing_team_read_team_name(message: Message, state: FSMContext):
    team_name = message.text
    await state.update_data(team_name=team_name)
    await message.answer("Write text to send (ParseMode.HTML)")
    await MailingTeamStates.waiting_text.set()


async def mailing_team_from_solution_callback(query: CallbackQuery, state: FSMContext):
    team_name = query.data.split("_")[-2]
    task_name = query.data.split("_")[-1]
    await state.update_data(team_name=team_name, task_name=task_name)
    # await query.answer("Write text to send (ParseMode.HTML)")
    await query.message.answer("Write text to send (ParseMode.HTML)")
    await MailingTeamStates.waiting_text.set()


async def mailing_team_read_text(message: Message, state: FSMContext):
    text = message.text
    task_name = (await state.get_data()).get("task_name", None)
    if task_name is not None:
        with get_db() as db:
            task: Task = db.query(Task).where(Task.name == task_name).first()
            if task is not None:
                await state.update_data(text=f"Manager of the task {task.name} sent you this message:\n\n{text}")
            else:
                await state.update_data(text=text)
        db.close()
    else:
        await state.update_data(text=text)
    kb = ReplyKeyboardMarkup().add(KeyboardButton("yes")).add(KeyboardButton("no"))
    await message.answer("Type yes/no to confirm/decline mailing", reply_markup=kb)
    await MailingTeamStates.waiting_confirm.set()


async def mailing_team_confirm(message: Message, state: FSMContext):
    if message.text == "yes":
        with get_db() as db:
            team: Team = db.query(Team).where(Team.name == (await state.get_data()).get("team_name", "Empty")).first()
            if team is None:
                await state.finish()
                await message.answer("No such team")
            users: list[User] = db.query(User).where(User.team_id == team.id).all()
        bot = BotHolder().bot
        text = (await state.get_data()).get("text", "Empty text")
        users = users if users is not None else []
        db.close()
        for user in users:
            try:
                await bot.send_message(user.chat_id, text, parse_mode=ParseMode.HTML)
            except:
                pass
        await message.answer("Completed", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Canceled", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@user_exists
@admin_method
async def get_users(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        users: list[User] = db.query(User).all()
    users = users if users is not None else []
    ans = ""
    for user in users:
        ans += f"{user.url} | @{user.username} | {user.role}\n"
    db.close()
    await message.answer(ans)


class ManagerStates(StatesGroup):
    waiting_task_name = State()


@user_exists
@admin_method
async def manager_start(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        tasks: list[Task] = db.query(Task).where(Task.with_manager == True).all()
    tasks = tasks if tasks is not None else []
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for task in tasks:
        kb.add(KeyboardButton(task.name))
    db.close()
    await message.answer(
        "Choose task to become manager of", reply_markup=kb
    )
    await ManagerStates.waiting_task_name.set()


async def manager_read_task(message: Message, state: FSMContext):
    task_name = message.text
    with get_db() as db:
        user: User = db.query(User).where(User.chat_id == message.chat.id).first()
        task: Task = db.query(Task).where(Task.name == task_name).first()
        if task is None:
            await state.finish()
            return await message.answer("No such task")
        if not task.with_manager:
            await state.finish()
            return await message.answer("Manager is not allowed for this task")

        task.manager_id = message.chat.id
        db.commit()
        db.refresh(task)
        await notify_admins(db, f"Now {user.line_info} is the manager of the task {task.name}")
    db.close()
    await state.finish()
    return await message.answer(f"Now you are manager of the {task.name} task")


async def solution_mark_checked(query: CallbackQuery, state: FSMContext):
    team_name = query.data.split("_")[-2]
    task_name = query.data.split("_")[-1]
    await query.message.edit_reply_markup(reply_markup=manager_checked_kb(team_name, task_name))


async def solution_mark_unchecked(query: CallbackQuery, state: FSMContext):
    team_name = query.data.split("_")[-2]
    task_name = query.data.split("_")[-1]
    await query.message.edit_reply_markup(reply_markup=manager_check_kb(team_name, task_name))


@user_exists
@admin_method
async def get_invite_tokens(message: Message, state: FSMContext):
    await state.finish()
    text = "Invite tokens:\n\n"
    with get_db() as db:
        teams: List[Team] = db.query(Team).all()
        teams.sort(key=lambda t: t.name)
        for team in teams:
            text += f"{hbold(team.name)}: {hspoiler(team.token)}\n"
    db.close()
    await message.answer(text, parse_mode=ParseMode.HTML)


@user_exists
@admin_method
async def build_results_start(message: Message, state: FSMContext):
    await state.finish()
    name = build_results()
    await message.answer_document(open(f'./results/{name}.xlsx', "rb"))
