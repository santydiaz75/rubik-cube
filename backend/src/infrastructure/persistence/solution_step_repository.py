from __future__ import annotations

from ...domain.game.entities import CubeStateStep
from .base import MongoRepositoryBase


class MongoSolutionStepRepository(MongoRepositoryBase):
    @property
    def collection(self):
        return self.db["cubeStates"]

    async def create_many(self, steps: list[CubeStateStep]) -> list[CubeStateStep]:
        if steps:
            self.collection.insert_many([step.to_document() for step in steps])
        return steps

    async def list_by_game(self, game_id: str) -> list[CubeStateStep]:
        cursor = self.collection.find({"idGame": game_id}).sort("movement", 1)
        return [CubeStateStep.from_document(document) for document in cursor]

    async def get_by_game_and_movement(self, game_id: str, movement: int) -> CubeStateStep | None:
        found = self.collection.find_one({"idGame": game_id, "movement": movement})
        return CubeStateStep.from_document(found) if found else None
