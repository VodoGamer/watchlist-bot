from abc import ABC

from sqlalchemy import Insert, Select
from sqlalchemy.orm import Session

from watchlist_bot.models import Base


class ABCRepository(ABC):
    session: Session


class BaseRepository[T: Base](ABCRepository):
    def __init__(self, session: Session):
        self.session = session

    def _select_or_insert(
        self, select_statement: Select[tuple[T]], insert_statement: Insert
    ) -> T:
        result = self.session.execute(select_statement)
        response = result.scalar_one_or_none()
        if response:
            return response
        self.session.execute(insert_statement)
        self.session.commit()
        result = self.session.execute(select_statement)
        return result.scalar_one()
