from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session

from hunt.db import get_db
from hunt.services import TaskManager

offline_tasks_btn = InlineKeyboardButton("🌏 IRL tasks", callback_data="offline_tasks_btn")
online_tasks_btn = InlineKeyboardButton("🤖 InBot tasks", callback_data="online_tasks_btn")
cosplay_btn = InlineKeyboardButton("🎭 Cosplay", callback_data="cosplay_btn")
secrets_btn = InlineKeyboardButton("🔍 Secrets", callback_data="secrets_btn")
songs_btn = InlineKeyboardButton("🎧 Song summarization", callback_data="songs_btn")
rhymes_btn = InlineKeyboardButton("📝 Rhyme time", callback_data="rhymes_btn")
quiz_btn = InlineKeyboardButton("⁉️ Quiz", callback_data="quiz_btn")

default_tasks_markup = (
    InlineKeyboardMarkup()
    .add(offline_tasks_btn)
    .add(online_tasks_btn)
    .add(cosplay_btn)
    .add(secrets_btn)
    .add(songs_btn)
    .add(rhymes_btn)
    .add(quiz_btn)
)


def offline_tasks_kb(db: Session, team_id: UUID):
    tasks = TaskManager().get_offline_tasks(db)
    kb = InlineKeyboardMarkup()
    for task in tasks:
        if task.usage > 0:
            txt = task.name
            if TaskManager().check_task_solved(db, task.id, team_id):
                txt = "✅ " + txt
            kb.add(InlineKeyboardButton(txt, callback_data="offline_task_" + str(task.id)))
    kb.add(InlineKeyboardButton("⏪ Back", callback_data="back_tasks"))
    return kb


def online_tasks_kb(db: Session, team_id: UUID):
    tasks = TaskManager().get_online_tasks(db)
    kb = InlineKeyboardMarkup()
    for task in tasks:
        if task.usage > 0:
            txt = task.name
            if TaskManager().check_task_solved(db, task.id, team_id):
                txt = "✅ " + txt
            kb.add(InlineKeyboardButton(txt, callback_data="online_task_" + str(task.id)))
    kb.add(InlineKeyboardButton("⏪ Back", callback_data="back_tasks"))
    return kb


def cosplay_tasks_kb(db: Session, team_id: UUID):
    tasks = TaskManager().get_cosplay_tasks(db)
    kb = InlineKeyboardMarkup()
    for task in tasks:
        if task.usage > 0:
            txt = task.name
            if TaskManager().check_task_solved(db, task.id, team_id):
                txt = "✅ " + txt
            kb.add(InlineKeyboardButton(txt, callback_data="cosplay_task_" + str(task.id)))
    kb.add(InlineKeyboardButton("⏪ Back", callback_data="back_tasks"))
    return kb


def secrets_tasks_kb(db: Session, team_id: UUID):
    tasks = TaskManager().get_secrets_tasks(db)
    solved_number, tasks_number = TaskManager().count_solved_tasks(db, tasks, team_id)
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            f"Found {solved_number}/{tasks_number} secrets", callback_data="empty"
        )
    )
    kb.add(InlineKeyboardButton("🗺️ Map", callback_data="map"))
    kb.add(InlineKeyboardButton("⏪ Back", callback_data="back_tasks"))
    return kb


def songs_tasks_kb(db: Session, team_id: UUID):
    tasks = TaskManager().get_songs_tasks(db)
    kb = InlineKeyboardMarkup()
    for task in tasks:
        if task.usage > 0:
            txt = task.name
            if TaskManager().check_task_solved(db, task.id, team_id):
                txt = "✅ " + txt
            kb.add(InlineKeyboardButton(txt, callback_data="song_task_" + str(task.id)))
    kb.add(InlineKeyboardButton("⏪ Back", callback_data="back_tasks"))
    return kb


def rhymes_tasks_kb(db: Session, team_id: UUID):
    tasks = TaskManager().get_rhymes_tasks(db)
    kb = InlineKeyboardMarkup()
    for task in tasks:
        if task.usage > 0:
            txt = task.name
            if TaskManager().check_task_solved(db, task.id, team_id):
                txt = "✅ " + txt
            kb.add(InlineKeyboardButton(txt, callback_data="rhyme_task_" + str(task.id)))
    kb.add(InlineKeyboardButton("⏪ Back", callback_data="back_tasks"))
    return kb


def back_kb(data: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("⏪ Back", callback_data="back_" + data)
    )


def manager_close_kb(data: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("✉️ Solve", callback_data=f"solve_task_{data}"),
        InlineKeyboardButton("❌ Close", callback_data="close")
    )


def manager_back_kb(solve_data: str, back_data: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("✉️ Solve", callback_data=f"solve_task_{solve_data}"),
        InlineKeyboardButton("⏪ Back", callback_data="back_" + back_data)
    )


def manager_check_kb(team_name: str, task_name: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Give points", callback_data=f"solution_check_yes_{team_name}_{task_name}"),
        InlineKeyboardButton("Send message", callback_data=f"solution_check_send_{team_name}_{task_name}"),
        InlineKeyboardButton("Mark checked", callback_data=f"solution_check_checked_{team_name}_{task_name}")
    )


def manager_checked_kb(team_name: str, task_name: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Checked", callback_data="Empty"),
        InlineKeyboardButton("Mark unchecked", callback_data=f"solution_check_unchecked_{team_name}_{task_name}")
    )


close_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("❌ Close", callback_data="close")
)

casino_bet_amount = InlineKeyboardMarkup() \
    .row(InlineKeyboardButton("10", callback_data="bet_amount_10"), InlineKeyboardButton("50", callback_data="bet_amount_50")) \
    .row(InlineKeyboardButton("100", callback_data="bet_amount_100"), InlineKeyboardButton("250", callback_data="bet_amount_250")) \
    .row(InlineKeyboardButton("500", callback_data="bet_amount_500"), InlineKeyboardButton("1000", callback_data="bet_amount_1000")) \

casino_bet_option = InlineKeyboardMarkup() \
    .add(InlineKeyboardButton("🟥 RED (x2)", callback_data="bet_option_red")) \
    .add(InlineKeyboardButton("⬛ BLACK (x2)", callback_data="bet_option_black")) \
    .add(InlineKeyboardButton("🟩 GREEN (x10)", callback_data="bet_option_green"))

casino_wait = InlineKeyboardMarkup().add(InlineKeyboardButton("🌪️ Wheel is spinning...", callback_data="empty"))
