from importlib.metadata import version

from telegrinder import Dispatch, Message
from telegrinder.rules import Command
from telegrinder.types import LinkPreviewOptions

dp = Dispatch()


@dp.message(Command("version"))
async def start(message: Message) -> None:

    await message.answer(
        f"Версия бота: {version('watchlist-bot')}\n\nИсходный текст проекта: https://github.com/VodoGamer/watchlist-bot",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
