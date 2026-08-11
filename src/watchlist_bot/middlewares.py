from telegrinder import ABCMiddleware
from telegrinder.node import UserId

from watchlist_bot.config import ALLOWED_USER_IDS


class AllowedUsersMiddleware(ABCMiddleware):
    async def pre(self, user_id: UserId) -> bool:
        return user_id in ALLOWED_USER_IDS
