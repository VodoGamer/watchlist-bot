from telegrinder import MESSAGE_FROM_USER, CallbackQuery, Dispatch, MessageCute
from telegrinder.rules import HasText, PayloadMarkupRule
from telegrinder.types import LinkPreviewOptions

from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


@dp.callback_query(PayloadMarkupRule("edit/<watch_entry_id:int>"))
async def handle_edit_description(
    callback_query: CallbackQuery, watch_entry_id: int, repository: DBRepositoryNode
) -> None:
    watch_entry = repository.watch_entry.get_by_id(watch_entry_id)
    message_id_to_edit = callback_query.message.unwrap().only(MessageCute).unwrap().message_id
    await callback_query.api.edit_message_text(
        text=f"Введите новое описание для {watch_entry.as_html()}:",
        chat_id=callback_query.chat_id.unwrap(),
        message_id=message_id_to_edit,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    answer, _ = await dp.message.wait(
        MESSAGE_FROM_USER(callback_query.from_user.id),
        release=HasText(),
    )
    repository.watch_entry.set_description(watch_entry_id, answer.text.unwrap())
    await callback_query.api.send_message(
        text=f"Описание для {watch_entry.as_html()} обновлено!",
        chat_id=callback_query.chat_id.unwrap(),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
