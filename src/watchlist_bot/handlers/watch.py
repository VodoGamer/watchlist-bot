from telegrinder import Dispatch, Message
from telegrinder.rules import Command

from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()


@dp.message(Command("watch"))
async def handle_watch(message: Message, repository: DBRepositoryNode) -> None:
    watch_list = repository.watch_entry.generate_watch_list()
    choice = dp.checkbox(
        message.chat.id,
        message="Выберите что вы закончили смотреть:",
        max_in_row=2,
        ready_text="Посмотрено!",
    )
    for watch_entry in watch_list:
        choice.add_option(
            watch_entry.id,
            f"{watch_entry.description or watch_entry.content}",
            f"✅ {watch_entry.description or watch_entry.content}",
        )
    chosen, message_id = await choice.wait(message.api)
    for key, value in chosen.items():
        if value == True:
            repository.watch_entry.mark_completed(key)

    await message.edit(text="Обновлено!", message_id=message_id)
