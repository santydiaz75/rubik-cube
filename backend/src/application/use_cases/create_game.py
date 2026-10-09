from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from ...domain.cube.entities import CubeState, ValidationIssue, apply_move_sequence, apply_move, is_solved
from ...domain.cube.validation import validate_cube
from ...domain.game.entities import CubeRecord, CubeStateStep, Game
from ...domain.user.entities import utc_now
from ..ports.cube_solver import CubeSolver
from ..ports.repositories import CubeRepository, GameRepository, SolutionStepRepository, UserRepository


class ApplicationError(Exception):
    def __init__(self, code: str, message: str, details: list[ValidationIssue] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or []


@dataclass(frozen=True)
class CreateGameResult:
    game: Game
    steps: list[CubeStateStep]


class CreateGameUseCase:
    def __init__(
        self,
        users: UserRepository,
        games: GameRepository,
        cubes: CubeRepository,
        solution_steps: SolutionStepRepository,
        solver: CubeSolver,
    ) -> None:
        self._users = users
        self._games = games
        self._cubes = cubes
        self._solution_steps = solution_steps
        self._solver = solver

    async def execute(self, user_id: str, cube_payload: dict[str, object]) -> CreateGameResult:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise ApplicationError(code="USER_NOT_FOUND", message="The provided userId does not exist")

        cube = CubeState.from_dict(cube_payload)
        validation_errors = validate_cube(cube)
        if validation_errors:
            raise ApplicationError(code="INVALID_CUBE", message="The provided cube is invalid", details=validation_errors)

        cube_id = str(uuid4())
        persisted_cube = CubeRecord(cube_id=cube_id, initial_state={**cube.to_dict(), "cubeId": cube_id})
        await self._cubes.create(persisted_cube)

        game = Game(
            game_id=str(uuid4()),
            user_id=user.user_id,
            cube_id=cube_id,
            created_at=utc_now(),
            score=0,
            status="created",
            current_step=0,
        )
        game = await self._games.create(game)

        if is_solved(cube):
            completed_game = Game(
                game_id=game.game_id,
                user_id=game.user_id,
                cube_id=game.cube_id,
                created_at=game.created_at,
                score=0,
                status="completed",
                current_step=0,
                error_message=None,
            )
            updated = await self._games.update(completed_game)
            return CreateGameResult(game=updated, steps=[])

        solving_game = Game(
            game_id=game.game_id,
            user_id=game.user_id,
            cube_id=game.cube_id,
            created_at=game.created_at,
            score=game.score,
            status="solving",
            current_step=0,
            error_message=None,
        )
        await self._games.update(solving_game)

        try:
            moves = await self._solver.solve(cube)
        except ValueError as exc:
            failed = Game(
                game_id=game.game_id,
                user_id=game.user_id,
                cube_id=game.cube_id,
                created_at=game.created_at,
                score=0,
                status="failed",
                current_step=0,
                error_message=str(exc),
            )
            await self._games.update(failed)
            raise ApplicationError(code="UNSOLVABLE_CUBE", message=str(exc)) from exc

        current_cube = CubeState(cube_id=cube_id, status=cube.status, faces=cube.faces)
        steps: list[CubeStateStep] = []
        for index, move in enumerate(moves, start=1):
            current_cube = apply_move(current_cube, move)
            steps.append(
                CubeStateStep(
                    cube_id=cube_id,
                    game_id=game.game_id,
                    movement=index,
                    notation=move,
                    cube_state=current_cube.to_dict(),
                )
            )

        if steps:
            await self._solution_steps.create_many(steps)

        completed = Game(
            game_id=game.game_id,
            user_id=game.user_id,
            cube_id=game.cube_id,
            created_at=game.created_at,
            score=len(moves),
            status="completed",
            current_step=0,
            error_message=None,
        )
        updated_game = await self._games.update(completed)
        return CreateGameResult(game=updated_game, steps=steps)
