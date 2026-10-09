from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_create_game_use_case, get_game_repository, get_solution_step_repository
from ..schemas.error import ErrorDetailModel, ErrorResponseModel
from ..schemas.game import CreateGameRequestModel, GameCreationResponseModel, GameSummaryModel, SolutionStepModel
from ...application.use_cases.create_game import ApplicationError, CreateGameUseCase
from ...infrastructure.persistence.game_repository import MongoGameRepository
from ...infrastructure.persistence.solution_step_repository import MongoSolutionStepRepository

router = APIRouter(prefix="/games", tags=["games"])


def _raise_application_error(error: ApplicationError) -> None:
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY if error.code == "UNSOLVABLE_CUBE" else status.HTTP_400_BAD_REQUEST
    details = [
        ErrorDetailModel(
            face=issue.locations[0].face if issue.locations else None,
            index=issue.locations[0].index if issue.locations else None,
            issue=issue.message,
        ).model_dump()
        for issue in error.details
    ]
    raise HTTPException(status_code=status_code, detail={"code": error.code, "message": error.message, "details": details})


@router.post("/", response_model=GameCreationResponseModel, status_code=status.HTTP_201_CREATED)
async def create_game(
    payload: CreateGameRequestModel,
    use_case: CreateGameUseCase = Depends(get_create_game_use_case),
) -> GameCreationResponseModel:
    try:
        result = await use_case.execute(user_id=payload.userId, cube_payload=payload.cube.model_dump())
    except ApplicationError as exc:
        _raise_application_error(exc)

    return GameCreationResponseModel(
        game=GameSummaryModel.from_domain(result.game),
        totalMoves=len(result.steps),
        steps=[SolutionStepModel.from_domain(step) for step in result.steps],
    )


@router.get("/{game_id}", response_model=GameSummaryModel)
async def get_game(
    game_id: str,
    games: MongoGameRepository = Depends(get_game_repository),
) -> GameSummaryModel:
    game = await games.get_by_id(game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return GameSummaryModel.from_domain(game)


@router.get("/{game_id}/steps", response_model=dict[str, object])
async def list_steps(
    game_id: str,
    steps_repo: MongoSolutionStepRepository = Depends(get_solution_step_repository),
) -> dict[str, object]:
    steps = await steps_repo.list_by_game(game_id)
    return {
        "gameId": game_id,
        "totalMoves": len(steps),
        "steps": [SolutionStepModel.from_domain(step).model_dump() for step in steps],
    }


@router.get("/{game_id}/steps/{movement}", response_model=SolutionStepModel)
async def get_step(
    game_id: str,
    movement: int,
    steps_repo: MongoSolutionStepRepository = Depends(get_solution_step_repository),
) -> SolutionStepModel:
    step = await steps_repo.get_by_game_and_movement(game_id, movement)
    if step is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Step not found")
    return SolutionStepModel.from_domain(step)
