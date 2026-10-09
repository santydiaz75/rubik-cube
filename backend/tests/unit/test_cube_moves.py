import pytest

from backend.src.domain.cube.entities import CubeState, apply_move, apply_move_sequence, is_solved
from backend.src.infrastructure.solver.rubik_solver_adapter import RubikSolverAdapter


def solved_cube() -> CubeState:
    return CubeState.from_dict(
        {
            "cubeId": "cube-moves",
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
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("move", ["U", "D", "L", "R", "F", "B"])
async def test_applied_solver_move_sequence_returns_cube_to_solved_state(move: str) -> None:
    cube = solved_cube()
    scrambled_cube = apply_move(cube, move)

    solution = await RubikSolverAdapter().solve(scrambled_cube)

    assert is_solved(apply_move_sequence(scrambled_cube, solution))
