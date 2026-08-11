from telegrinder.types import BotCommand

from watchlist_bot.client import api

bot_commands: list[BotCommand] = [
    BotCommand("start", "📺"),
    BotCommand("save", "Сохранить для просмотра"),
    BotCommand("list", "Что посмотреть?"),
    BotCommand("watch", "Отметить прогресс"),
    BotCommand("rate", "Оценить отсмотренное"),
    BotCommand("viewed", "Что уже посмотрели?"),
]


async def update_bot_commands():
    await api.set_my_commands(commands=bot_commands)
