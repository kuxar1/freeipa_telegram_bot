from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Start command')
        ],
        scope=BotCommandScopeDefault()
    )
