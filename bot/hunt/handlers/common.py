import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from hunt.db.connection.session import get_db
from hunt.utils import send_answer, user_exists
from hunt.replies.replies import replies


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(
        start, Text(startswith="start", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        start, Text(endswith="start", ignore_case=True), state="*"
    )
    dp.register_message_handler(cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cancel, Text(startswith="cancel", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        cancel, Text(endswith="cancel", ignore_case=True), state="*"
    )
    dp.register_message_handler(info, commands="info", state="*")
    dp.register_message_handler(
        info, Text(startswith="info", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        info, Text(endswith="info", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        info, Text(startswith="help", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        info, Text(endswith="help", ignore_case=True), state="*"
    )
    dp.register_message_handler(support, commands="support", state="*")
    dp.register_message_handler(
        support, Text(startswith="support", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        support, Text(endswith="support", ignore_case=True), state="*"
    )
    dp.register_message_handler(send_map, commands="map", state="*")
    dp.register_message_handler(
        send_map, Text(startswith="map", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        send_map, Text(endswith="map", ignore_case=True), state="*"
    )

    dp.register_message_handler(rofl, commands="rofl", state="*")
    dp.register_message_handler(rofl, Text(equals="rofl", ignore_case=True), state="*")


@user_exists
async def start(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        await send_answer(db, message.chat.id, "start")


@user_exists
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        await send_answer(db, message.chat.id, "cancel")


@user_exists
async def info(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        await send_answer(db, message.chat.id, "info")


@user_exists
async def support(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        await send_answer(db, message.chat.id, "support")


@user_exists
async def send_map(message: Message, state: FSMContext):
    await state.finish()
    with get_db() as db:
        await send_answer(db, message.chat.id, "map")


@user_exists
async def rofl(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(random.choice(replies["rofls"]))
