from backend.src.domain.cube.entities import CubeState, apply_move, is_solved
from backend.src.domain.cube.validation import validate_cube


def solved_cube() -> CubeState:
    return CubeState.from_dict(
        {
            "cubeId": "cube-1",
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


def test_validate_cube_accepts_solved_state() -> None:
    cube = solved_cube()
    assert validate_cube(cube) == []
    assert is_solved(cube) is True


def test_validate_cube_rejects_color_count_mismatch() -> None:
    cube = solved_cube()
    faces = cube.to_dict()["faces"]
    faces["u"][0] = "red"
    invalid = CubeState.from_dict({"cubeId": "cube-2", "status": "in-progress", "faces": faces})
    issues = validate_cube(invalid)
    assert any(issue.code == "COLOR_COUNT" for issue in issues)


def test_apply_move_changes_state() -> None:
    moved = apply_move(solved_cube(), "R")
    assert moved != solved_cube()
