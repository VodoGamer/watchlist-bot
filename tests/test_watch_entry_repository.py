import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from watchlist_bot.models import Base, User
from watchlist_bot.repotitories.watch_entry import WatchEntryRepository


class WatchEntryRepositoryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.user = User(id=1, first_name="Test")
        self.session.add(self.user)
        self.session.commit()
        self.repository = WatchEntryRepository(self.session)

    def tearDown(self) -> None:
        self.session.close()
        self.engine.dispose()

    def test_generate_unrated_list_returns_only_completed_unrated_entries(self) -> None:
        pending = self.repository.create(self.user, "Pending")
        unrated = self.repository.create(self.user, "Unrated")
        rated = self.repository.create(self.user, "Rated")
        self.repository.mark_completed(unrated.id)
        self.repository.mark_completed(rated.id)
        self.assertTrue(self.repository.set_rating(rated.id, 8))

        result = self.repository.generate_unrated_list()

        self.assertEqual([entry.id for entry in result], [unrated.id])
        self.assertIsNone(pending.watched_at)

    def test_set_rating_only_accepts_valid_rating_for_unrated_completed_entry(
        self,
    ) -> None:
        pending = self.repository.create(self.user, "Pending")
        completed = self.repository.create(self.user, "Completed")
        self.repository.mark_completed(completed.id)

        self.assertFalse(self.repository.set_rating(pending.id, 7))
        self.assertFalse(self.repository.set_rating(completed.id, 0))
        self.assertTrue(self.repository.set_rating(completed.id, 10))
        self.assertFalse(self.repository.set_rating(completed.id, 9))

        self.session.refresh(completed)
        self.assertEqual(completed.rating, 10)


if __name__ == "__main__":
    unittest.main()
