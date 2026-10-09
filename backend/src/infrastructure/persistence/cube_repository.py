from __future__ import annotations

from ...domain.game.entities import CubeRecord
from .base import MongoRepositoryBase


class MongoCubeRepository(MongoRepositoryBase):
    @property
    def collection(self):
        return self.db["cubes"]

    async def create(self, cube: CubeRecord) -> CubeRecord:
        self.collection.insert_one(cube.to_document())
        return cube

    async def get_by_id(self, cube_id: str) -> CubeRecord | None:
        found = self.collection.find_one({"idCube": cube_id})
        return CubeRecord.from_document(found) if found else None
