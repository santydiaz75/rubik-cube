from __future__ import annotations

from ..ports.repositories import UserRepository
from ...domain.user.entities import User


class RegisterPlayerUseCase:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, username: str, fullname: str) -> User:
        return await self._users.upsert(username=username, fullname=fullname)
