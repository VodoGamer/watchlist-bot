from telegrinder import MESSAGE_FROM_USER, CallbackQuery, Dispatch
from telegrinder.rules import HasText, PayloadMarkupRule

from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


@dp.callback_query(PayloadMarkupRule("edit/<watch_entry_id:int>"))
async def handle_edit_description(
    callback_query: CallbackQuery, watch_entry_id: int, repository: DBRepositoryNode
) -> None:
    watch_entry = repository.watch_entry.get_by_id(watch_entry_id)
    await callback_query.api.send_message(
        text=f'Введите новое описание для "{watch_entry.content}":',
        chat_id=callback_query.chat_id.unwrap(),
    )
    answer, _ = await dp.message.wait(
        MESSAGE_FROM_USER(callback_query.from_user.id),
        release=HasText(),
    )
    repository.watch_entry.set_description(watch_entry_id, answer.text.unwrap())
    await callback_query.api.send_message(
        text=f'Описание для "{watch_entry.content}" обновлено!',
        chat_id=callback_query.chat_id.unwrap(),
    )
