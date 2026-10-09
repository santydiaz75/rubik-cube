from __future__ import annotations

from pydantic import BaseModel, Field


class CubeFacesModel(BaseModel):
    u: list[str] = Field(min_length=9, max_length=9)
    d: list[str] = Field(min_length=9, max_length=9)
    f: list[str] = Field(min_length=9, max_length=9)
    b: list[str] = Field(min_length=9, max_length=9)
    l: list[str] = Field(min_length=9, max_length=9)
    r: list[str] = Field(min_length=9, max_length=9)


class CubeStateModel(BaseModel):
    cubeId: str
    status: str
    faces: CubeFacesModel
