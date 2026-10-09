from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

GameStatus = Literal["created", "solving", "completed", "failed"]


@dataclass(frozen=True)
class Game:
    game_id: str
    user_id: str
    cube_id: str
    created_at: datetime
    score: int
    status: GameStatus
    current_step: int
    error_message: str | None = None

    def to_document(self) -> dict[str, object]:
        return {
            "idGame": self.game_id,
            "userId": self.user_id,
            "idCube": self.cube_id,
            "createdAt": self.created_at,
            "score": self.score,
            "status": self.status,
            "currentStep": self.current_step,
            "errorMessage": self.error_message,
        }

    @classmethod
    def from_document(cls, document: dict[str, object]) -> "Game":
        return cls(
            game_id=str(document["idGame"]),
            user_id=str(document["userId"]),
            cube_id=str(document["idCube"]),
            created_at=document["createdAt"],  # type: ignore[arg-type]
            score=int(document.get("score", 0)),
            status=str(document.get("status", "created")),  # type: ignore[arg-type]
            current_step=int(document.get("currentStep", 0)),
            error_message=document.get("errorMessage"),  # type: ignore[arg-type]
        )


@dataclass(frozen=True)
class CubeRecord:
    cube_id: str
    initial_state: dict[str, object]

    def to_document(self) -> dict[str, object]:
        return {"idCube": self.cube_id, "initialState": self.initial_state}

    @classmethod
    def from_document(cls, document: dict[str, object]) -> "CubeRecord":
        return cls(cube_id=str(document["idCube"]), initial_state=document["initialState"])  # type: ignore[arg-type]


@dataclass(frozen=True)
class CubeStateStep:
    cube_id: str
    game_id: str
    movement: int
    notation: str
    cube_state: dict[str, object]

    def to_document(self) -> dict[str, object]:
        return {
            "idCube": self.cube_id,
            "idGame": self.game_id,
            "movement": self.movement,
            "notation": self.notation,
            "cubeState": self.cube_state,
        }

    @classmethod
    def from_document(cls, document: dict[str, object]) -> "CubeStateStep":
        return cls(
            cube_id=str(document["idCube"]),
            game_id=str(document["idGame"]),
            movement=int(document["movement"]),
            notation=str(document["notation"]),
            cube_state=document["cubeState"],  # type: ignore[arg-type]
        )
