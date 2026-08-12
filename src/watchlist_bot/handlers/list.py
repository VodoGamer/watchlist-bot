from telegrinder import Dispatch, Message
from telegrinder.rules import Command
from telegrinder.types import LinkPreviewOptions

from watchlist_bot.models import WatchEntry
from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


def _format_watch_entries(watch_list: list[WatchEntry]) -> str:
    return "\n".join(
        [f"{index + 1}. {watch_entry.content}" for index, watch_entry in enumerate(watch_list)]
    )


@dp.message(Command("list"))
async def handle_list(message: Message, repository: DBRepositoryNode) -> None:
    watch_list = repository.watch_entry.generate_watch_list()
    if len(watch_list) == 0:
        await message.answer("Список просмотра пуст, добавьте новый контент командой /save")
        return
    watch_list_str = _format_watch_entries(watch_list)
    await message.answer(
        watch_list_str,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@dp.message(Command("viewed"))
async def handle_viewed(message: Message, repository: DBRepositoryNode) -> None:
    watched_list = repository.watch_entry.generate_watch_list(is_watched=True)
    if len(watched_list) == 0:
        await message.answer(
            "Список просмотренного пуст, чтобы отметить прогресс используйте команду /watch"
        )
        return
    watched_list_str = _format_watch_entries(watched_list)
    await message.answer(
        watched_list_str,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
