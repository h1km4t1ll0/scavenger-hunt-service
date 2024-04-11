from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="/cancel", description="[Cancel] Cancel current action"
        ),
        BotCommand(
            command="/help",
            description="[Help] Commands list",
        ),
        BotCommand(
            command="/info",
            description="[Info] Some information about this quest",
        ),
        # BotCommand(
        #     command="/create_team", description="[Create Team]"
        # ),
        BotCommand(command="/join_team", description="[Join Team]"),
        BotCommand(command="/leave_team", description="[Leave Team]"),
        BotCommand(command="/my_team", description="[My Team] Information about your team"),
        BotCommand(
            command="/tasks", description="[Tasks] Show tasks"
        ),
        BotCommand(
            command="/flag", description="[Flag] Pass some flag to earn points"
        ),
        # BotCommand(
        #     command="/casino", description="[Casino] Play casino"
        # ),
        BotCommand(
            command="/scoreboard", description="[Scoreboard] Show scoreboard"
        ),
        BotCommand(
            command="/map", description="[Map] Show map"
        ),
        BotCommand(
            command="/rofl", description="[Rofl] Random rofl from the bot, or sth else..."
        ),
    ]
    await bot.set_my_commands(commands)
