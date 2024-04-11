import asyncio
import logging
from aiohttp import web
from aiogram.dispatcher.webhook import get_new_configured_app
from hunt.bot_holder import BotHolder
from hunt.handlers import (
    register_handlers_admin,
    register_handlers_common,
    register_handlers_task,
    register_handlers_team,
    register_handlers_test,
    register_handlers_casino,
    register_handlers_quiz,
)
from hunt.utils import set_commands
#from webhook import app, bot_holder
from webhook import app, bot_holder, on_startup, on_shutdown

async def main():
    bot = BotHolder()

    await set_commands(bot.bot)
    register_handlers_common(bot.dp)
    register_handlers_admin(bot.dp)
    register_handlers_team(bot.dp)
    register_handlers_task(bot.dp)
    # register_handlers_casino(bot.dp)
    register_handlers_test(bot.dp)
    register_handlers_quiz(bot.dp)

    await bot.dp.start_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = get_new_configured_app(dispatcher=bot_holder.dp, path='/' + bot_holder.settings.BOT_TOKEN)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(
        app,
        host='0.0.0.0',  #f"https://{bot_holder.settings.BOT_WEBHOOK_URL}",
        port=int(bot_holder.settings.BOT_PORT)
    )

