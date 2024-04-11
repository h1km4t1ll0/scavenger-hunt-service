from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from singleton_decorator import singleton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from hunt.config.get_settings import get_settings


@singleton
class BotHolder:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.bot = Bot(settings.BOT_TOKEN)
        self.dp: Dispatcher = Dispatcher(self.bot, storage=MongoStorage(host=settings.MONGO_HOST, port=settings.MONGO_PORT, db_name=settings.MONGO_DB))
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
