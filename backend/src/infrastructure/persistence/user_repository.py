from __future__ import annotations

from uuid import uuid4

from pymongo import ReturnDocument

from ...domain.user.entities import User, normalize_username, utc_now
from .base import MongoRepositoryBase


class MongoUserRepository(MongoRepositoryBase):
    @property
    def collection(self):
        return self.db["users"]

    async def upsert(self, username: str, fullname: str) -> User:
        normalized = normalize_username(username)
        clean_fullname = fullname.strip()
        if not clean_fullname:
            raise ValueError("fullname must not be empty")

        existing = self.collection.find_one({"username": normalized})
        now = utc_now()
        if existing is None:
            document = {
                "userId": str(uuid4()),
                "username": normalized,
                "fullname": clean_fullname,
                "score": 0,
                "createdAt": now,
                "updatedAt": now,
            }
            self.collection.insert_one(document)
            return User.from_document(document)

        updated = self.collection.find_one_and_update(
            {"username": normalized},
            {"$set": {"fullname": clean_fullname, "updatedAt": now}},
            return_document=ReturnDocument.AFTER,
        )
        if updated is None:
            raise RuntimeError("failed to update user")
        return User.from_document(updated)

    async def get_by_id(self, user_id: str) -> User | None:
        found = self.collection.find_one({"userId": user_id})
        return User.from_document(found) if found else None
