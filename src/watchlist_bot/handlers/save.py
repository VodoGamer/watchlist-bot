from typing import Final

from telegrinder import (
    MESSAGE_FROM_USER,
    Dispatch,
    InlineButton,
    InlineKeyboard,
    Message,
    MessageReplyHandler,
)
from telegrinder.modules import logger
from telegrinder.rules import ABCRule, Argument, Command, HasText
from telegrinder.types import InlineKeyboardMarkup

from watchlist_bot.config import ALLOWED_USER_IDS
from watchlist_bot.nodes import DBRepositoryNode, DBUserNode

dp = Dispatch()

MAX_CONTENT_LENGTH: Final[int] = 256


def get_actions_keyboard(watch_entry_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboard()
    kb.add(InlineButton("Добавить описание", callback_data=f"edit/{watch_entry_id}"))
    kb.add(InlineButton("🗑 Отменить", callback_data=f"send/{watch_entry_id}/undo"))
    return kb.get_markup()


def text_validator(text: str, max_length: int = MAX_CONTENT_LENGTH) -> str | None:
    if len(text) <= max_length:
        return text


class IsTextLong(ABCRule, requires=[HasText()]):
    async def check(
        self, message: Message, max_length: int = MAX_CONTENT_LENGTH
    ) -> bool:
        return bool(text_validator(message.text.unwrap(), max_length))


@dp.message(Command("save", Argument("content", [text_validator])))
async def handle_quick_save(
    message: Message, content: str, repository: DBRepositoryNode, user: DBUserNode
) -> None:
    watch_entry = repository.watch_entry.create(user, content)
    await message.answer(
        f'"{content}" сохранено в список для просмотра!',
        reply_markup=get_actions_keyboard(watch_entry.id),
    )
    squad_user_ids = set(ALLOWED_USER_IDS) - {user.id}
    for squad_user_id in squad_user_ids:
        logger.info(f"Send distribution message to user_id: {squad_user_id}")
        await message.api.send_message(
            chat_id=squad_user_id,
            text=f'Участник {user.first_name} добавил "{watch_entry.content}" в список просмотра',
        )


@dp.message(Command("save"))
async def handle_save(
    message: Message, repository: DBRepositoryNode, user: DBUserNode
) -> None:
    await message.answer("Введите, то, что хотите сохранить в список для просмотра:")
    msg, _ = await dp.message.wait(
        MESSAGE_FROM_USER(message.from_user.id),
        release=HasText() & IsTextLong(),
        on_miss=MessageReplyHandler(
            f"Длина содержимого не должна привышать {MAX_CONTENT_LENGTH} символов",
            as_reply=True,
        ),
    )
    watch_entry = repository.watch_entry.create(user, msg.text.unwrap())
    await message.answer(
        f'"{msg.text.unwrap()}" сохранено в список для просмотра!',
        reply_markup=get_actions_keyboard(watch_entry.id),
    )
