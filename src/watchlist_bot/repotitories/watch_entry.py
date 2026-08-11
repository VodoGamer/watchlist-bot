from sqlalchemy import delete, insert, select, update

from watchlist_bot.models import User, WatchEntry
from watchlist_bot.repotitories.base import BaseRepository


class WatchEntryRepository(BaseRepository):
    def create(
        self, user: User, content: str, description: str | None = None
    ) -> WatchEntry:
        stmt = (
            insert(WatchEntry)
            .values(content=content, description=description, author_id=user.id)
            .returning(WatchEntry)
        )
        watch_entry = self.session.execute(stmt).scalar_one()
        self.session.commit()
        return watch_entry

    def get_by_id(self, watch_entry_id: int) -> WatchEntry:
        stmt = select(WatchEntry).where(WatchEntry.id == watch_entry_id)
        return self.session.execute(stmt).scalar_one()

    def set_description(self, watch_entry_id: int, new_description: str | None) -> None:
        stmt = (
            update(WatchEntry)
            .where(WatchEntry.id == watch_entry_id)
            .values(description=new_description)
        )
        self.session.execute(stmt)
        self.session.commit()

    def delete(self, watch_entry_id: int) -> None:
        stmt = delete(WatchEntry).where(WatchEntry.id == watch_entry_id)
        self.session.execute(stmt)
        self.session.commit()

    def generate_watch_list(self) -> list[WatchEntry]:
        stmt = select(WatchEntry).where(WatchEntry.watched_at == None)
        return list(self.session.execute(stmt).scalars())
