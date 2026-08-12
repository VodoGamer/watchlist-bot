from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from telegrinder import Message
from telegrinder.modules import logger
from telegrinder.node import UserId, global_node, scalar_node

from watchlist_bot.config import DB_PATH
from watchlist_bot.models import User
from watchlist_bot.repotitories.factory import RepositoryFactory


@global_node
@scalar_node
class DBEngineNode:
    @classmethod
    def __compose__(cls) -> Generator[Engine]:
        engine = create_engine(DB_PATH)
        logger.info("sqlalchemy engine was created")
        yield engine
        logger.debug("sqlalchemy engine was disposed")
        engine.dispose()


@scalar_node
class DBSessionNode:
    @classmethod
    def __compose__(cls, engine: DBEngineNode) -> Generator[Session]:
        session = Session(engine)
        logger.info("sqlalchemy session was started")
        yield session
        logger.debug("sqlalchemy session was closed")
        session.close()


@scalar_node
class DBRepositoryNode:
    @classmethod
    def __compose__(cls, session: DBSessionNode) -> RepositoryFactory:
        return RepositoryFactory(session)


@scalar_node
class DBUserNode:
    @classmethod
    def __compose__(cls, repo: DBRepositoryNode, message: Message, user_id: UserId) -> User:
        return repo.user.get_or_register(user_id, message.from_user.first_name)
