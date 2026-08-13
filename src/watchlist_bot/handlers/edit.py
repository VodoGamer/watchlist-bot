from telegrinder import MESSAGE_FROM_USER, CallbackQuery, Dispatch, Message, MessageCute
from telegrinder.rules import Command, HasText, PayloadMarkupRule
from telegrinder.types import LinkPreviewOptions

from watchlist_bot.models import WatchEntry
from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


@dp.message(Command("edit"))
async def handle_edit_description(message: Message, repository: DBRepositoryNode) -> None:
    watch_list = repository.watch_entry.generate_watch_list()
    choice = dp.choice(
        message.chat_id, "Выберите контент для изменения:", max_in_row=2, ready_text="Изменить!"
    )
    for index, watch_entry in enumerate(watch_list):
        choice.add_option(
            watch_entry.id,
            f"{watch_entry.description or watch_entry.content}",
            f"✅ {watch_entry.description or watch_entry.content}",
            is_picked=index == 0,
        )
    choiced_id, message_id = await choice.wait(message.api)
    choiced_watch_entry: WatchEntry | None = next(
        filter(lambda entry: entry.id == choiced_id, watch_list), None
    )
    if not choiced_watch_entry:
        await message.api.edit_message_text(
            text="Произошла ошибка при обработке результата выбора!",
            chat_id=message.chat_id,
            message_id=message_id,
        )
        return
    await message.api.edit_message_text(
        text=f"Введите новое описание для {choiced_watch_entry.as_html()}:",
        chat_id=message.chat_id,
        message_id=message_id,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    new_description, _ = await dp.message.wait(
        MESSAGE_FROM_USER(message.from_user.id), release=HasText()
    )
    repository.watch_entry.set_description(choiced_watch_entry.id, new_description.text.unwrap())
    await message.answer(
        text=f"Описание для {choiced_watch_entry.as_html()} обновлено!",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@dp.callback_query(PayloadMarkupRule("edit/<watch_entry_id:int>"))
async def handle_callback_edit_description(
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
