from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Literal

FaceName = Literal["u", "d", "f", "b", "l", "r"]
CubeColor = Literal["white", "yellow", "green", "blue", "orange", "red"]
CubeStatus = Literal["in-progress", "solved"]

FACE_NAMES: tuple[FaceName, ...] = ("u", "d", "f", "b", "l", "r")
SOLVER_FACE_ORDER: tuple[FaceName, ...] = ("u", "r", "f", "d", "l", "b")
ALLOWED_COLORS: tuple[CubeColor, ...] = ("white", "yellow", "green", "blue", "orange", "red")
MOVE_NOTATIONS = {
    "U",
    "U'",
    "U2",
    "D",
    "D'",
    "D2",
    "L",
    "L'",
    "L2",
    "R",
    "R'",
    "R2",
    "F",
    "F'",
    "F2",
    "B",
    "B'",
    "B2",
}

Vector = tuple[int, int, int]


@dataclass(frozen=True)
class StickerLocation:
    face: FaceName
    index: int


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    locations: tuple[StickerLocation, ...] = ()


@dataclass(frozen=True)
class CubeState:
    cube_id: str
    status: CubeStatus
    faces: dict[FaceName, tuple[CubeColor, ...]]

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "CubeState":
        cube_id = str(payload["cubeId"])
        status = _normalize_status(str(payload.get("status", "in-progress")))
        raw_faces = payload.get("faces")
        if not isinstance(raw_faces, dict):
            raise ValueError("faces must be an object")
        normalized_faces: dict[FaceName, tuple[CubeColor, ...]] = {}
        for face in FACE_NAMES:
            raw_face = raw_faces.get(face)
            if not isinstance(raw_face, list):
                raise ValueError(f"face {face} must be a list")
            normalized_faces[face] = tuple(_normalize_color(color) for color in raw_face)
        return cls(cube_id=cube_id, status=status, faces=normalized_faces)

    def to_dict(self) -> dict[str, object]:
        return {
            "cubeId": self.cube_id,
            "status": self.status,
            "faces": {face: list(colors) for face, colors in self.faces.items()},
        }


def _normalize_status(status: str) -> CubeStatus:
    lowered = status.strip().lower().replace(" ", "-")
    if lowered not in {"in-progress", "solved"}:
        raise ValueError("invalid cube status")
    return "solved" if lowered == "solved" else "in-progress"


def _normalize_color(value: object) -> CubeColor:
    if not isinstance(value, str):
        raise ValueError("invalid color")
    lowered = value.strip().lower()
    if lowered not in ALLOWED_COLORS:
        raise ValueError(f"unsupported color: {value}")
    return lowered  # type: ignore[return-value]


def count_colors(cube: CubeState) -> Counter[str]:
    return Counter(color for face in FACE_NAMES for color in cube.faces.get(face, ()))


def is_complete(cube: CubeState) -> bool:
    return all(len(cube.faces.get(face, ())) == 9 for face in FACE_NAMES)


def is_solved(cube: CubeState) -> bool:
    return all(len(set(cube.faces[face])) == 1 for face in FACE_NAMES)


def solver_string(cube: CubeState) -> str:
    center_mapping = {
        cube.faces["u"][4]: "U",
        cube.faces["r"][4]: "R",
        cube.faces["f"][4]: "F",
        cube.faces["d"][4]: "D",
        cube.faces["l"][4]: "L",
        cube.faces["b"][4]: "B",
    }
    if len(center_mapping) != 6:
        raise ValueError("cube centers must be unique")

    letters: list[str] = []
    for face in SOLVER_FACE_ORDER:
        for color in cube.faces[face]:
            mapped = center_mapping.get(color)
            if mapped is None:
                raise ValueError(f"color {color} does not match any center")
            letters.append(mapped)
    return "".join(letters)


def cube_from_solver_string(cube_id: str, facelets: str, face_color_map: dict[str, CubeColor] | None = None) -> CubeState:
    if len(facelets) != 54:
        raise ValueError("solver string must be 54 characters")
    colors_by_face = face_color_map or {
        "U": "white",
        "R": "red",
        "F": "green",
        "D": "yellow",
        "L": "orange",
        "B": "blue",
    }
    faces: dict[FaceName, tuple[CubeColor, ...]] = {}
    ranges = {
        "u": facelets[0:9],
        "r": facelets[9:18],
        "f": facelets[18:27],
        "d": facelets[27:36],
        "l": facelets[36:45],
        "b": facelets[45:54],
    }
    for face, section in ranges.items():
        faces[face] = tuple(colors_by_face[letter] for letter in section)  # type: ignore[assignment]
    status: CubeStatus = "solved" if all(len(set(values)) == 1 for values in faces.values()) else "in-progress"
    return CubeState(cube_id=cube_id, status=status, faces=faces)


def parse_moves(solution: str) -> list[str]:
    cleaned = solution.strip()
    return cleaned.split() if cleaned else []


def apply_move_sequence(cube: CubeState, moves: Iterable[str]) -> CubeState:
    state = cube
    for move in moves:
        state = apply_move(state, move)
    return state


def apply_move(cube: CubeState, move: str) -> CubeState:
    if move not in MOVE_NOTATIONS:
        raise ValueError(f"unsupported move notation: {move}")

    face = move[0]
    turns = 2 if move.endswith("2") else 1
    turns = 3 if move.endswith("'") else turns
    facelets = list(solver_string(cube))
    face_color_map = {
        "U": cube.faces["u"][4],
        "R": cube.faces["r"][4],
        "F": cube.faces["f"][4],
        "D": cube.faces["d"][4],
        "L": cube.faces["l"][4],
        "B": cube.faces["b"][4],
    }
    for _ in range(turns):
        facelets = _apply_clockwise_turn(facelets, face)
    return cube_from_solver_string(cube.cube_id, "".join(facelets), face_color_map)


def _apply_clockwise_turn(facelets: list[str], face: str) -> list[str]:
    axis, layer_value, direction = _turn_definition(face)
    rotated = facelets.copy()
    for index, (position, normal) in INDEX_TO_STICKER.items():
        if _position_matches_layer(position, axis, layer_value):
            new_position = _rotate_vector(position, axis, direction)
            new_normal = _rotate_vector(normal, axis, direction)
            rotated_index = STICKER_TO_INDEX[(new_position, new_normal)]
            rotated[rotated_index] = facelets[index]
        else:
            rotated[index] = facelets[index]
    return rotated


def _turn_definition(face: str) -> tuple[str, int, int]:
    if face == "U":
        return ("y", 1, -1)
    if face == "D":
        return ("y", -1, 1)
    if face == "R":
        return ("x", 1, -1)
    if face == "L":
        return ("x", -1, 1)
    if face == "F":
        return ("z", 1, -1)
    if face == "B":
        return ("z", -1, 1)
    raise ValueError(f"unsupported face turn: {face}")


def _position_matches_layer(position: Vector, axis: str, layer_value: int) -> bool:
    axis_index = {"x": 0, "y": 1, "z": 2}[axis]
    return position[axis_index] == layer_value


def _rotate_vector(vector: Vector, axis: str, direction: int) -> Vector:
    x, y, z = vector
    if axis == "x":
        return (x, -direction * z, direction * y) if direction == 1 else (x, z, -y)
    if axis == "y":
        return (z, y, -x) if direction == 1 else (-z, y, x)
    if axis == "z":
        return (-y, x, z) if direction == 1 else (y, -x, z)
    raise ValueError(f"unsupported axis: {axis}")


def _build_index_maps() -> tuple[dict[int, tuple[Vector, Vector]], dict[tuple[Vector, Vector], int]]:
    index_to_sticker: dict[int, tuple[Vector, Vector]] = {}
    sticker_to_index: dict[tuple[Vector, Vector], int] = {}
    start_index = 0
    for face in SOLVER_FACE_ORDER:
        for row in range(3):
            for column in range(3):
                position, normal = _face_coordinates(face, row, column)
                index_to_sticker[start_index] = (position, normal)
                sticker_to_index[(position, normal)] = start_index
                start_index += 1
    return index_to_sticker, sticker_to_index


def _face_coordinates(face: FaceName, row: int, column: int) -> tuple[Vector, Vector]:
    if face == "u":
        return ((column - 1, 1, row - 1), (0, 1, 0))
    if face == "r":
        return ((1, 1 - row, 1 - column), (1, 0, 0))
    if face == "f":
        return ((column - 1, 1 - row, 1), (0, 0, 1))
    if face == "d":
        return ((column - 1, -1, 1 - row), (0, -1, 0))
    if face == "l":
        return ((-1, 1 - row, column - 1), (-1, 0, 0))
    if face == "b":
        return ((1 - column, 1 - row, -1), (0, 0, -1))
    raise ValueError(f"unsupported face {face}")


INDEX_TO_STICKER, STICKER_TO_INDEX = _build_index_maps()
