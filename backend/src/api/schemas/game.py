from __future__ import annotations

from pydantic import BaseModel, Field

from ...domain.game.entities import CubeStateStep, Game
from .cube import CubeStateModel


class CreateGameRequestModel(BaseModel):
    userId: str
    cube: CubeStateModel


class GameSummaryModel(BaseModel):
    idGame: str
    userId: str
    idCube: str
    status: str
    score: int
    currentStep: int
    createdAt: str
    errorMessage: str | None = None

    @classmethod
    def from_domain(cls, game: Game) -> "GameSummaryModel":
        return cls(
            idGame=game.game_id,
            userId=game.user_id,
            idCube=game.cube_id,
            status=game.status,
            score=game.score,
            currentStep=game.current_step,
            createdAt=game.created_at.isoformat(),
            errorMessage=game.error_message,
        )


class SolutionStepModel(BaseModel):
    idGame: str
    idCube: str
    movement: int = Field(ge=1)
    notation: str
    cubeState: dict[str, object]

    @classmethod
    def from_domain(cls, step: CubeStateStep) -> "SolutionStepModel":
        return cls(
            idGame=step.game_id,
            idCube=step.cube_id,
            movement=step.movement,
            notation=step.notation,
            cubeState=step.cube_state,
        )


class GameCreationResponseModel(BaseModel):
    game: GameSummaryModel
    totalMoves: int
    steps: list[SolutionStepModel]
