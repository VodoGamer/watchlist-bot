import os
from typing import Final, cast, get_args

from dotenv import load_dotenv
from kungfu import Error, Nothing, Ok, Option, Result, Some
from telegrinder.modules import LoggerLevel

load_dotenv()


def _get_secret_value(key: str) -> Option[str]:
    value = os.getenv(key)
    return Some(value) if value is not None else Nothing()


def _is_logger_level(level: str) -> Result[LoggerLevel, str]:
    logger_levels = get_args(LoggerLevel.__value__)
    if level in logger_levels:
        return Ok(cast(LoggerLevel, level))
    return Error(
        f"Logger level is incorrect! Available levels: {logger_levels}. Provided: {level}"
    )


TELEGRAM_BOT_TOKEN: Final[str] = _get_secret_value("TELEGRAM_BOT_TOKEN").unwrap()
DB_PATH: Final[str] = _get_secret_value("DB_PATH").unwrap()

ALLOWED_USER_IDS: Final[list[int]] = (
    _get_secret_value("ALLOWED_USER_IDS")
    .map(lambda str: str.strip().split(","))
    .map(lambda ids: list(map(int, ids)))
    .unwrap()
)

LOGGING_LEVEL: Final[LoggerLevel] = (
    _get_secret_value("LOGGING_LEVEL").cast(Ok, Error).then(_is_logger_level).unwrap_or("INFO")
)
