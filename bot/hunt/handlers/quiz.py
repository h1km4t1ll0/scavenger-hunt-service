from datetime import datetime, timedelta

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, InputFile, Message, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from hunt import BotHolder
from hunt.replies import replies
from hunt.config import get_settings
from hunt.db.connection.session import get_db
from hunt.db.models import Team, User, Task, SolvedQuiz, Results, SolvedTasks
from hunt.keyboard import (
    back_kb,
    close_kb,
    cosplay_tasks_kb,
    default_tasks_markup,
    offline_tasks_kb,
    online_tasks_kb,
    secrets_tasks_kb, manager_close_kb, manager_back_kb, manager_check_kb,
)
from hunt.services import TaskActionResult, TaskManager, TeamManager
from hunt.utils import notify_team, send_answer, user_exists, user_in_team


questions = [
    "1. Which language family does English belong to?\n\n"
    "a) Romance\n"
    "b) Slavic\n"
    "c) Germanic\n"
    "d) Celtic",

    "2. Who were the earliest inhabitants of the British Isles that had a language whose linguistic remnants are still known?\n\n"
    "a) The Romans\n"
    "b) The Celts\n"
    "c) The Vikings\n"
    "d) The Slavs",

    "3. Which famous playwright added over 1,700 words to the English language?\n\n"
    "a) Harold Pinter\n"
    "b) William Shakespeare\n"
    "c) Oscar Wilde\n"
    "d) Arthur Miller",

    "4. Which of the following is NOT a real geographical place name in the UK?\n\n"
    "a) Llanfair­pwllgwyngyll­gogery­chwyrn­drobwll­llan­tysilio­gogo­goch\n"
    "b) Pity Me\n"
    "c) Ceann a Tuath Loch Baghasdail\n"
    "d) Snoddinghamshiretonwell",

    "5. Which of the following words holds the record for the most meanings in the English language?\n\n"
    "a) Set\n"
    "b) Run\n"
    "c) Go\n"
    "d) Take",

    "6. What is the most commonly used letter in the English language?\n\n"
    "a) E\n"
    "b) A\n"
    "c) T\n"
    "d) O",

    "7. What did the Norman Conquest of 1066 bring to England?\n\n"
    "a) A resurgence of Old English\n"
    "b) A shift from Latin to French\n"
    "c) A period of linguistic stability\n"
    "d) A decline in French influence",

    "8. How many French words were incorporated into English during the Norman occupation?\n\n"
    "a) About 1,000\n"
    "b) About 4,000\n"
    "c) About 10,000\n"
    "d) About 30,000",

    "9. Which of the following is the most widely used English word throughout the world?\n\n"
    "a) Dollar\n"
    "b) Okay\n"
    "c) Internet\n"
    "d) Scavenger hunt",

    "10. What is the official language of The United States?\n\n"
    "a) English\n"
    "b) French\n"
    "c) English and Spanish\n"
    "d) No official language",

    "11. What product did the Victorians refer to as 'Little Bags of Mystery'?\n\n"
    "a) Candies\n"
    "b) Sausages\n"
    "c) Pastries\n"
    "d) Children"
]

correct_answers = "cbbdaabcbdb"

answer_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("a", callback_data="quiz_answer_a"),
    InlineKeyboardButton("b", callback_data="quiz_answer_b"),
    InlineKeyboardButton("c", callback_data="quiz_answer_c"),
    InlineKeyboardButton("d", callback_data="quiz_answer_d"),
)


start_quiz_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Start Quiz", callback_data="start_quiz"),
    InlineKeyboardButton("⏪ Back", callback_data="back_tasks")
)

solved_quiz_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Solved!", callback_data="back_tasks")
)


def register_handlers_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz_info, commands="quiz", state="*")
    dp.register_callback_query_handler(
        quiz_next_step, Text(startswith="quiz_answer_"), state="*"
    )
    dp.register_callback_query_handler(
        quiz_start_check, Text(equals="start_quiz"), state="*"
    )


@user_exists
@user_in_team
async def quiz_info(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "ATTENTION! Your team has only one attempt to solve this task. "
        "To get point you have to give correct replies. (Max points = 3)\n"
        "Also your points depends on the time you spend:\n"
        "- less than <b>2 minutes</b> <i>+1 point</i>\n"
        "- less than <b>1 minute</b> <i>+2 points</i>\n"
        "If you have less than 3 correct answers, you won't get additional points(((\n"
        "As a result the maximum number of points for this task is <b>3 + 2 = 5</b>\n\n"
        "Be careful! Using this button you will start your single try. "
        "Your team won't be able to solve it one more time after that. Good luck!",
        parse_mode=ParseMode.HTML,
        reply_markup=start_quiz_kb,
    )


async def quiz_info_from_btn(query: CallbackQuery, state: FSMContext):
    await quiz_info(query.message, state)


async def quiz_start_check(query: CallbackQuery, state: FSMContext):
    try:
        await state.finish()
        with get_db() as db:
            user: User = db.query(User).where(User.chat_id == query.message.chat.id).first()
            team: Team = db.query(Team).where(Team.id == user.team_id).first()
            solved_quiz: SolvedQuiz = db.query(SolvedQuiz).where(SolvedQuiz.team_id == team.id).first()
            if solved_quiz is not None:
                return await query.answer("Sorry, your team had already tried this Quiz, you have no more attempts")

            solved_quiz = SolvedQuiz(team_id=team.id)
            db.add(solved_quiz)
            db.commit()
        db.close()
        await state.update_data(quiz_start=datetime.now(), question_number=0)
        await quiz_next_step(query, state)
    except Exception as e:
        print(e)
        db.close()


async def quiz_next_step(query: CallbackQuery, state: FSMContext):
    try:
        question_number = (await state.get_data()).get("question_number", 0)
        if 0 < question_number < 10:
            cur_answers = (await state.get_data()).get("quiz_answers", "")
            await state.update_data(quiz_answers=f"{cur_answers}{query.data.split('_')[-1]}")
        if question_number == 10:
            cur_answers = (await state.get_data()).get("quiz_answers", "")
            await state.update_data(quiz_answers=f"{cur_answers}{query.data.split('_')[-1]}")
            return await quiz_end(query, state)
        await query.message.edit_text(questions[question_number])
        await query.message.edit_reply_markup(answer_kb)
        await state.update_data(question_number=question_number + 1)
    except Exception as e:
        print(e)


async def quiz_end(query: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        quiz_answers = data.get("quiz_answers", "bababbaaab")
        score = 0
        for i, quiz_answer in enumerate(quiz_answers):
            if quiz_answer == correct_answers[i]:
                score += 1
        time_spent = datetime.now() - data.get('quiz_start', datetime.now() - timedelta(minutes=5))
        text_prefix = f"Congrats! Your results:\n" \
                      f"Time - {time_spent.seconds} seconds\n" \
                      f"Correct answers - {score}/{len(questions)}\n\n"
        with get_db() as db:
            user: User = db.query(User).where(User.chat_id == query.message.chat.id).first()
            team: Team = db.query(Team).where(Team.id == user.team_id).first()
            team.amount += int(score / 3)
            text_prefix = text_prefix + f"You've got {int(score / 3)} points for correct answers!\n"
            db.commit()
        db.close()

        if score >= 3:
            with get_db() as db:
                user: User = db.query(User).where(User.chat_id == query.message.chat.id).first()
                team: Team = db.query(Team).where(Team.id == user.team_id).first()

                if time_spent.seconds > 120:
                    text_prefix += "Sorry, but you have spent too much time to get additional points..."
                elif time_spent.seconds > 60:
                    text_prefix += "You earned 1 additional point, because you were fast!"
                    team.amount += 1
                else:
                    text_prefix += "You earned 2 additional points, because you were very fast!"
                    team.amount += 2
                db.commit()
            db.close()

        await query.message.edit_text(text_prefix)
        await query.message.edit_reply_markup(solved_quiz_kb)
        await state.finish()
    except Exception as e:
        print(e)
        db.close()
