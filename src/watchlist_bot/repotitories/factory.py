from sqlalchemy.orm import Session

from watchlist_bot.repotitories.user import UserRepository
from watchlist_bot.repotitories.watch_entry import WatchEntryRepository


class RepositoryFactory:
    def __init__(self, session: Session):
        self._session = session

        self.user = UserRepository(self._session)
        self.watch_entry = WatchEntryRepository(self._session)
