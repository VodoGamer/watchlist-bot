from telegrinder import API, Telegrinder, Token
from telegrinder.modules import setup_logger

from watchlist_bot.config import LOGGING_LEVEL, TELEGRAM_BOT_TOKEN
from watchlist_bot.middlewares import AllowedUsersMiddleware

setup_logger(level=LOGGING_LEVEL)
api = API(token=Token(TELEGRAM_BOT_TOKEN))
bot = Telegrinder(api)
bot.dispatch.register_middleware(AllowedUsersMiddleware)
