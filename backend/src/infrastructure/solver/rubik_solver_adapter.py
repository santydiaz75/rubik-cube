from __future__ import annotations

import kociemba

from ...domain.cube.entities import CubeState, parse_moves, solver_string


class RubikSolverAdapter:
    async def solve(self, cube: CubeState) -> list[str]:
        try:
            solution = kociemba.solve(solver_string(cube))
        except Exception as exc:  # pragma: no cover - third-party error surface
            raise ValueError("The provided cube state is not physically solvable") from exc
        return parse_moves(solution)
