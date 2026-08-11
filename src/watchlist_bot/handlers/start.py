from telegrinder import Dispatch, Message
from telegrinder.rules import Text

from watchlist_bot.commands import bot_commands

dp = Dispatch()


@dp.message(Text("/start"))
async def start(message: Message) -> None:
    commands_str = ""
    for bot_command in bot_commands:
        commands_str += f"/{bot_command.command} — {bot_command.description}\n"
    await message.answer(
        "Бот для совместного ведения списка просмотренного!\n\n"
        f"Доступные команды:\n{commands_str}"
    )
