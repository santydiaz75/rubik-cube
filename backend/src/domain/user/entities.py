from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True)
class User:
    user_id: str
    username: str
    fullname: str
    score: int
    created_at: datetime
    updated_at: datetime

    def to_document(self) -> dict[str, object]:
        return {
            "userId": self.user_id,
            "username": self.username,
            "fullname": self.fullname,
            "score": self.score,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    @classmethod
    def from_document(cls, document: dict[str, object]) -> "User":
        return cls(
            user_id=str(document["userId"]),
            username=str(document["username"]),
            fullname=str(document["fullname"]),
            score=int(document.get("score", 0)),
            created_at=document["createdAt"],  # type: ignore[arg-type]
            updated_at=document["updatedAt"],  # type: ignore[arg-type]
        )


def normalize_username(username: str) -> str:
    normalized = username.strip().lower()
    if not normalized:
        raise ValueError("username must not be empty")
    return normalized
