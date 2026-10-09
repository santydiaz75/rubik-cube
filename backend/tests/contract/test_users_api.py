from fastapi.testclient import TestClient

from backend.src.api.dependencies import get_register_player_use_case
from backend.src.api.main import app
from backend.src.domain.user.entities import User, utc_now


class StubRegisterPlayerUseCase:
    async def execute(self, username: str, fullname: str) -> User:
        now = utc_now()
        return User(user_id="user-1", username=username, fullname=fullname, score=0, created_at=now, updated_at=now)


def test_upsert_user_contract() -> None:
    app.dependency_overrides[get_register_player_use_case] = lambda: StubRegisterPlayerUseCase()
    client = TestClient(app)

    response = client.put("/users/alice", json={"fullname": "Alice Smith"})

    assert response.status_code == 200
    assert response.json()["username"] == "alice"
    assert response.json()["fullname"] == "Alice Smith"
    app.dependency_overrides.clear()
