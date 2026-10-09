from __future__ import annotations

from collections import Counter, defaultdict

from .entities import ALLOWED_COLORS, FACE_NAMES, CubeState, StickerLocation, ValidationIssue, count_colors, is_complete


def validate_cube(cube: CubeState) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    missing_faces = [face for face in FACE_NAMES if face not in cube.faces]
    if missing_faces:
        issues.append(
            ValidationIssue(
                code="MISSING_FACE",
                message=f"Missing cube faces: {', '.join(missing_faces)}",
            )
        )
        return issues

    invalid_lengths = [face for face in FACE_NAMES if len(cube.faces[face]) != 9]
    if invalid_lengths:
        issues.extend(
            ValidationIssue(
                code="INVALID_FACE_SIZE",
                message=f"Face {face.upper()} must contain exactly 9 stickers",
                locations=tuple(StickerLocation(face=face, index=index) for index in range(len(cube.faces[face]), 9)),
            )
            for face in invalid_lengths
        )

    if not is_complete(cube):
        issues.append(ValidationIssue(code="MISSING_STICKER", message="All 54 stickers must be filled before solving"))

    color_locations: dict[str, list[StickerLocation]] = defaultdict(list)
    for face in FACE_NAMES:
        for index, color in enumerate(cube.faces[face]):
            if color not in ALLOWED_COLORS:
                issues.append(
                    ValidationIssue(
                        code="INVALID_COLOR",
                        message=f"Unsupported color {color!r} at {face.upper()}[{index}]",
                        locations=(StickerLocation(face=face, index=index),),
                    )
                )
            else:
                color_locations[color].append(StickerLocation(face=face, index=index))

    color_counts: Counter[str] = count_colors(cube)
    for color in ALLOWED_COLORS:
        if color_counts[color] != 9:
            issues.append(
                ValidationIssue(
                    code="COLOR_COUNT",
                    message=f"Color {color} must appear exactly 9 times; found {color_counts[color]}",
                    locations=tuple(color_locations[color]),
                )
            )

    center_colors = {cube.faces[face][4] for face in FACE_NAMES if len(cube.faces[face]) > 4}
    if len(center_colors) != 6:
        issues.append(
            ValidationIssue(
                code="CENTER_DUPLICATE",
                message="All six center stickers must be different colors",
            )
        )

    return issues
