from __future__ import annotations

from fastapi import Depends

from ..application.use_cases.create_game import CreateGameUseCase
from ..application.use_cases.register_player import RegisterPlayerUseCase
from ..infrastructure.persistence.cube_repository import MongoCubeRepository
from ..infrastructure.persistence.game_repository import MongoGameRepository
from ..infrastructure.persistence.solution_step_repository import MongoSolutionStepRepository
from ..infrastructure.persistence.user_repository import MongoUserRepository
from ..infrastructure.solver.rubik_solver_adapter import RubikSolverAdapter


def get_user_repository() -> MongoUserRepository:
    return MongoUserRepository()


def get_game_repository() -> MongoGameRepository:
    return MongoGameRepository()


def get_cube_repository() -> MongoCubeRepository:
    return MongoCubeRepository()


def get_solution_step_repository() -> MongoSolutionStepRepository:
    return MongoSolutionStepRepository()


def get_solver() -> RubikSolverAdapter:
    return RubikSolverAdapter()


def get_register_player_use_case(users: MongoUserRepository = Depends(get_user_repository)) -> RegisterPlayerUseCase:
    return RegisterPlayerUseCase(users)


def get_create_game_use_case(
    users: MongoUserRepository = Depends(get_user_repository),
    games: MongoGameRepository = Depends(get_game_repository),
    cubes: MongoCubeRepository = Depends(get_cube_repository),
    solution_steps: MongoSolutionStepRepository = Depends(get_solution_step_repository),
    solver: RubikSolverAdapter = Depends(get_solver),
) -> CreateGameUseCase:
    return CreateGameUseCase(users, games, cubes, solution_steps, solver)
