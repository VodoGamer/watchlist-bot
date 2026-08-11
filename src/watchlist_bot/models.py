from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=lambda: datetime.now(tz=UTC),
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)

    watch_entries: Mapped[list[WatchEntry]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id}, first_name={self.first_name})"


class WatchEntry(Base):
    __tablename__ = "watch_entry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    watched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rating: Mapped[int | None] = mapped_column(Integer)

    author: Mapped[User] = relationship(back_populates="watch_entries")

    def __repr__(self) -> str:
        return f"WatchEntry(id={self.id}, content={self.content}, author_id={self.author_id})"
