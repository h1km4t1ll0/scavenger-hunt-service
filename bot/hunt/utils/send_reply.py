from aiogram import Bot, types
from aiogram.types import InputFile, ParseMode, InputMedia, InputMediaPhoto
from sqlalchemy.orm import Session

from hunt import BotHolder
from hunt.replies import replies
from hunt.config import get_settings
from hunt.utils.kb_from_state import kb_from_state


async def send_answer(db: Session, chat_id: int, answer_name: str):
    bot: Bot = BotHolder().bot
    reply = replies[answer_name]
    for message in reply:
        if message["type"] == "text":
            await bot.send_message(
                chat_id,
                message["text"],
                parse_mode=ParseMode.HTML,
                reply_markup=kb_from_state(db, chat_id),
            )
        elif message["type"] == "map":
            media = types.MediaGroup()
            for img in message["src"]:
                media.attach_photo(InputFile(get_settings().SRC_PREFIX + img), img)
            await bot.send_message(
                chat_id,
                message["caption"],
                parse_mode=ParseMode.HTML
            )
            await bot.send_media_group(
                chat_id,
                media=media
            )
        elif message["type"] == "photo":
            photo = InputFile(get_settings().SRC_PREFIX + message["src"])
            await bot.send_photo(
                chat_id,
                photo,
                caption=message["caption"]
            )
        elif message["type"] == "sticker":
            await bot.send_sticker(
                chat_id,
                message["id"]
            )
