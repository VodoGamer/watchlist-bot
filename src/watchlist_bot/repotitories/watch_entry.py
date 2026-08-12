from datetime import UTC, datetime

from sqlalchemy import delete, insert, select, update

from watchlist_bot.models import User, WatchEntry
from watchlist_bot.repotitories.base import BaseRepository


class WatchEntryRepository(BaseRepository):
    def create(self, user: User, content: str, description: str | None = None) -> WatchEntry:
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

    def generate_watch_list(self, is_watched: bool = False) -> list[WatchEntry]:
        stmt = select(WatchEntry)

        if is_watched:
            stmt = stmt.where(WatchEntry.watched_at.is_not(None)).order_by(WatchEntry.watched_at)
        else:
            stmt = stmt.where(WatchEntry.watched_at.is_(None)).order_by(WatchEntry.created_at)

        return list(self.session.execute(stmt).scalars())

    def generate_unrated_list(self) -> list[WatchEntry]:
        stmt = (
            select(WatchEntry)
            .where(
                WatchEntry.watched_at.is_not(None),
                WatchEntry.rating.is_(None),
            )
            .order_by(WatchEntry.watched_at)
        )
        return list(self.session.execute(stmt).scalars())

    def get_unrated_by_id(self, watch_entry_id: int) -> WatchEntry | None:
        stmt = select(WatchEntry).where(
            WatchEntry.id == watch_entry_id,
            WatchEntry.watched_at.is_not(None),
            WatchEntry.rating.is_(None),
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def mark_completed(self, watch_entry_id: int) -> None:
        stmt = (
            update(WatchEntry)
            .where(WatchEntry.id == watch_entry_id)
            .values(watched_at=datetime.now(tz=UTC))
        )
        self.session.execute(stmt)
        self.session.commit()

    def set_rating(self, watch_entry_id: int, rating: int) -> bool:
        if rating not in range(1, 11):
            return False

        stmt = (
            update(WatchEntry)
            .where(
                WatchEntry.id == watch_entry_id,
                WatchEntry.watched_at.is_not(None),
                WatchEntry.rating.is_(None),
            )
            .values(rating=rating)
        )
        result = self.session.execute(stmt)
        self.session.commit()
        return bool(result.scalar_one_or_none())
