from __future__ import annotations

from typing import Protocol

from ...domain.cube.entities import CubeState


class CubeSolver(Protocol):
    async def solve(self, cube: CubeState) -> list[str]:
        """Return the ordered move sequence required to solve the cube."""
