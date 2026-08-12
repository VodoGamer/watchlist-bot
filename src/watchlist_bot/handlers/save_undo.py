from telegrinder import CallbackQuery, Dispatch, MessageCute
from telegrinder.rules import PayloadMarkupRule
from telegrinder.types import LinkPreviewOptions

from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


@dp.callback_query(PayloadMarkupRule("send/<watch_entry_id:int>/undo"))
async def handle_undo_watch_entry(
    callback_query: CallbackQuery, watch_entry_id: int, repository: DBRepositoryNode
) -> None:
    watch_entry = repository.watch_entry.get_by_id(watch_entry_id)
    repository.watch_entry.delete(watch_entry_id)
    message_id_to_edit = callback_query.message.unwrap().only(MessageCute).unwrap().message_id
    await callback_query.api.edit_message_text(
        text=f'"{watch_entry.content}" удалён из списка просмотра',
        chat_id=callback_query.chat_id.unwrap(),
        message_id=message_id_to_edit,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
