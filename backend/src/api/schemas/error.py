from __future__ import annotations

from pydantic import BaseModel


class ErrorDetailModel(BaseModel):
    face: str | None = None
    index: int | None = None
    issue: str | None = None


class ErrorResponseModel(BaseModel):
    code: str
    message: str
    details: list[ErrorDetailModel] = []
