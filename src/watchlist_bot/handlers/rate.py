from typing import Final

from telegrinder import CallbackQuery, Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.rules import Command, PayloadMarkupRule
from telegrinder.types import InlineKeyboardMarkup

from watchlist_bot.nodes import DBRepositoryNode

dp = Dispatch()

MIN_RATING: Final[int] = 1
MAX_RATING: Final[int] = 10


def get_watch_entries_keyboard(
    watch_entries: dict[int, str],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    for watch_entry_id, content in watch_entries.items():
        keyboard.add(
            InlineButton(content, callback_data=f"rate/{watch_entry_id}"),
        ).row()
    return keyboard.get_markup()


def get_rating_keyboard(watch_entry_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    for rating in range(MIN_RATING, MAX_RATING + 1):
        keyboard.add(
            InlineButton(str(rating), callback_data=f"rate/{watch_entry_id}/{rating}"),
        )
        if rating == 5:
            keyboard.row()
    return keyboard.get_markup()


@dp.message(Command("rate"))
async def handle_rate(message: Message, repository: DBRepositoryNode) -> None:
    watch_entries = repository.watch_entry.generate_unrated_list()
    if not watch_entries:
        await message.answer("Нет просмотренного без оценки.")
        return

    await message.answer(
        "Выберите, что хотите оценить:",
        reply_markup=get_watch_entries_keyboard(
            {watch_entry.id: watch_entry.content for watch_entry in watch_entries},
        ),
    )


@dp.callback_query(PayloadMarkupRule("rate/<watch_entry_id:int>"))
async def handle_rate_choice(
    callback_query: CallbackQuery,
    watch_entry_id: int,
    repository: DBRepositoryNode,
) -> None:
    watch_entry = repository.watch_entry.get_unrated_by_id(watch_entry_id)
    if watch_entry is None:
        await callback_query.answer(
            "Эту запись уже нельзя оценить.",
            show_alert=True,
        )
        return

    await callback_query.edit_text(
        text=f'Оцените "{watch_entry.content}" от {MIN_RATING} до {MAX_RATING}:',
        reply_markup=get_rating_keyboard(watch_entry_id),
    )
    await callback_query.answer()


@dp.callback_query(
    PayloadMarkupRule("rate/<watch_entry_id:int>/<rating:int>"),
)
async def handle_rating(
    callback_query: CallbackQuery,
    watch_entry_id: int,
    rating: int,
    repository: DBRepositoryNode,
) -> None:
    if not repository.watch_entry.set_rating(watch_entry_id, rating):
        await callback_query.answer(
            "Не удалось сохранить оценку.",
            show_alert=True,
        )
        return

    watch_entry = repository.watch_entry.get_by_id(watch_entry_id)
    await callback_query.edit_text(
        text=f'"{watch_entry.content}" оценено на {rating}/{MAX_RATING}.',
    )
    await callback_query.answer()
