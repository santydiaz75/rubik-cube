from uuid import uuid4

import pytest

from backend.src.application.use_cases.create_game import ApplicationError, CreateGameUseCase
from backend.src.domain.game.entities import CubeRecord, CubeStateStep, Game
from backend.src.domain.user.entities import User, utc_now


class FakeUserRepository:
    def __init__(self) -> None:
        now = utc_now()
        self.user = User(user_id="user-1", username="alice", fullname="Alice", score=0, created_at=now, updated_at=now)

    async def upsert(self, username: str, fullname: str) -> User:
        return self.user

    async def get_by_id(self, user_id: str) -> User | None:
        return self.user if user_id == self.user.user_id else None


class FakeGameRepository:
    def __init__(self) -> None:
        self.games: dict[str, Game] = {}

    async def create(self, game: Game) -> Game:
        self.games[game.game_id] = game
        return game

    async def update(self, game: Game) -> Game:
        self.games[game.game_id] = game
        return game

    async def get_by_id(self, game_id: str) -> Game | None:
        return self.games.get(game_id)


class FakeCubeRepository:
    def __init__(self) -> None:
        self.cubes: dict[str, CubeRecord] = {}

    async def create(self, cube: CubeRecord) -> CubeRecord:
        self.cubes[cube.cube_id] = cube
        return cube

    async def get_by_id(self, cube_id: str) -> CubeRecord | None:
        return self.cubes.get(cube_id)


class FakeSolutionStepRepository:
    def __init__(self) -> None:
        self.steps: list[CubeStateStep] = []

    async def create_many(self, steps: list[CubeStateStep]) -> list[CubeStateStep]:
        self.steps.extend(steps)
        return steps

    async def list_by_game(self, game_id: str) -> list[CubeStateStep]:
        return [step for step in self.steps if step.game_id == game_id]

    async def get_by_game_and_movement(self, game_id: str, movement: int) -> CubeStateStep | None:
        return next((step for step in self.steps if step.game_id == game_id and step.movement == movement), None)


class FakeSolver:
    async def solve(self, cube) -> list[str]:
        return ["R", "U"]


def solved_cube_payload() -> dict[str, object]:
    return {
        "cubeId": str(uuid4()),
        "status": "solved",
        "faces": {
            "u": ["white"] * 9,
            "d": ["yellow"] * 9,
            "f": ["green"] * 9,
            "b": ["blue"] * 9,
            "l": ["orange"] * 9,
            "r": ["red"] * 9,
        },
    }


@pytest.mark.asyncio
async def test_create_game_returns_zero_moves_for_solved_cube() -> None:
    use_case = CreateGameUseCase(
        users=FakeUserRepository(),
        games=FakeGameRepository(),
        cubes=FakeCubeRepository(),
        solution_steps=FakeSolutionStepRepository(),
        solver=FakeSolver(),
    )

    result = await use_case.execute("user-1", solved_cube_payload())

    assert result.game.score == 0
    assert result.steps == []


@pytest.mark.asyncio
async def test_create_game_rejects_unknown_user() -> None:
    use_case = CreateGameUseCase(
        users=FakeUserRepository(),
        games=FakeGameRepository(),
        cubes=FakeCubeRepository(),
        solution_steps=FakeSolutionStepRepository(),
        solver=FakeSolver(),
    )

    with pytest.raises(ApplicationError):
        await use_case.execute("missing-user", solved_cube_payload())
