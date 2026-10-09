from __future__ import annotations

from ...domain.game.entities import Game
from .base import MongoRepositoryBase


class MongoGameRepository(MongoRepositoryBase):
    @property
    def collection(self):
        return self.db["games"]

    async def create(self, game: Game) -> Game:
        self.collection.insert_one(game.to_document())
        return game

    async def update(self, game: Game) -> Game:
        self.collection.update_one({"idGame": game.game_id}, {"$set": game.to_document()}, upsert=True)
        return game

    async def get_by_id(self, game_id: str) -> Game | None:
        found = self.collection.find_one({"idGame": game_id})
        return Game.from_document(found) if found else None
