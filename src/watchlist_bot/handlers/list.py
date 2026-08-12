from collections.abc import Callable

from telegrinder import Dispatch, Message
from telegrinder.rules import Command
from telegrinder.tools.formatting.html import italic
from telegrinder.types import LinkPreviewOptions

from watchlist_bot.models import WatchEntry
from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


def _format_watch_entry(watch_entry: WatchEntry) -> str:
    return watch_entry.as_html() + italic(f" ({watch_entry.author.first_name})")


def _format_watched_entry(watch_entry: WatchEntry) -> str:
    return watch_entry.as_html() + italic(f" ({watch_entry.watched_at:%Y-%m-%d %H:%M:%S})")


def _format_watch_entries(
    watch_list: list[WatchEntry], formatter: Callable[[WatchEntry], str]
) -> str:
    return "\n".join(
        [f"{index + 1}. {formatter(watch_entry)}" for index, watch_entry in enumerate(watch_list)]
    )


@dp.message(Command("list"))
async def handle_list(message: Message, repository: DBRepositoryNode) -> None:
    watch_list = repository.watch_entry.generate_watch_list(join_author=True)
    if len(watch_list) == 0:
        await message.answer("Список просмотра пуст, добавьте новый контент командой /save")
        return
    watch_list_str = _format_watch_entries(watch_list, _format_watch_entry)
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
    watched_list_str = _format_watch_entries(watched_list, _format_watched_entry)
    await message.answer(
        watched_list_str,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
