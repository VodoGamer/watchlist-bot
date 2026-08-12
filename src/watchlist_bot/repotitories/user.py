from sqlalchemy import insert, select, update

from watchlist_bot.models import User
from watchlist_bot.repotitories.base import BaseRepository


class UserRepository(BaseRepository):
    def get_or_register(self, id: int, first_name: str) -> User:
        select_stmt = select(User).where(User.id == id)
        user = self.session.execute(select_stmt).scalar_one_or_none()

        if not user:
            insert_stmt = insert(User).values(id=id).returning(User)
            user = self.session.execute(insert_stmt).scalar_one()
            self.session.commit()

        if user.first_name != first_name:
            update_stmt = (
                update(User).where(User.id == id).values(first_name=first_name).returning(User)
            )
            user = self.session.execute(update_stmt).scalar_one()
            self.session.commit()
        return user
