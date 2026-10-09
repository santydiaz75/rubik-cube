from __future__ import annotations

from pydantic import BaseModel, Field

from ...domain.user.entities import User


class UserUpsertRequestModel(BaseModel):
    fullname: str = Field(min_length=1)


class UserResponseModel(BaseModel):
    userId: str
    username: str
    fullname: str
    score: int

    @classmethod
    def from_domain(cls, user: User) -> "UserResponseModel":
        return cls(userId=user.user_id, username=user.username, fullname=user.fullname, score=user.score)
