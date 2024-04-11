import asyncio
from aiohttp import web
import logging
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.types import ContentTypes

from hunt import BotHolder
from hunt.handlers import (register_handlers_common, register_handlers_admin, register_handlers_team,
                           register_handlers_task, register_handlers_test, register_handlers_quiz)
from hunt.utils import set_commands

bot_holder = BotHolder()
webhook_url = f"https://{bot_holder.settings.BOT_WEBHOOK_URL}/{bot_holder.settings.BOT_TOKEN}"


async def on_startup(app):
    await set_commands(bot_holder.bot)
    register_handlers_common(bot_holder.dp)
    register_handlers_admin(bot_holder.dp)
    register_handlers_team(bot_holder.dp)
    register_handlers_task(bot_holder.dp)
    # register_handlers_casino(bot.dp)
    # register_handlers_test(bot_holder.dp)
    register_handlers_quiz(bot_holder.dp)
    webhook = await bot_holder.bot.get_webhook_info()

    if webhook.url != webhook_url:
        # If URL doesnt match current - remove webhook
        logging.info("Webhoot set!")
        if not webhook.url:
            await bot_holder.bot.delete_webhook()

        # Set new URL for webhook
        await bot_holder.bot.set_webhook(webhook_url)


async def on_shutdown(app):
    """
    Graceful shutdown. This method is recommended by aiohttp docs.
    """
    # Remove webhook.
    await bot_holder.bot.delete_webhook()

    # Close Redis connection.
    await bot_holder.dp.storage.close()
    await bot_holder.dp.storage.wait_closed()


app = get_new_configured_app(dispatcher=bot_holder.dp, path='/' + bot_holder.settings.BOT_TOKEN)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
