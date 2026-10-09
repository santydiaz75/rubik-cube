from __future__ import annotations

from pymongo.database import Database

from .mongo_client import get_database


class MongoRepositoryBase:
    def __init__(self, database: Database | None = None) -> None:
        self._database = database or get_database()

    @property
    def db(self) -> Database:
        return self._database
