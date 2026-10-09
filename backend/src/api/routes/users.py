from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..dependencies import get_register_player_use_case
from ..schemas.user import UserResponseModel, UserUpsertRequestModel
from ...application.use_cases.register_player import RegisterPlayerUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/{username}", response_model=UserResponseModel, status_code=status.HTTP_200_OK)
async def upsert_user(
    username: str,
    payload: UserUpsertRequestModel,
    use_case: RegisterPlayerUseCase = Depends(get_register_player_use_case),
) -> UserResponseModel:
    user = await use_case.execute(username=username, fullname=payload.fullname)
    return UserResponseModel.from_domain(user)
