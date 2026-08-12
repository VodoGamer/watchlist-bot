from telegrinder import (
    Dispatch,
    Message,
)
from telegrinder.rules import Command

from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


@dp.message(Command("list"))
async def handle_list(message: Message, repository: DBRepositoryNode) -> None:
    watch_list = repository.watch_entry.generate_watch_list()
    watch_list_str = [
        f"{index + 1}. {watch_entry.content}" for index, watch_entry in enumerate(watch_list)
    ]
    await message.answer(
        "\n".join(watch_list_str),
    )
