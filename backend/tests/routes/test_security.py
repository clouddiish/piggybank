import pytest
from httpx import AsyncClient

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.integration
class TestSecurityRoutes:
    @pytest.mark.anyio
    async def test_login__valid_credentials(self, client_fixture: AsyncClient) -> None:
        payload = {"username": settings.initial_admin_email, "password": settings.initial_admin_password}
        response = await client_fixture.post("/token", data=payload)

        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

    @pytest.mark.anyio
    async def test_login__invalid_password(self, client_fixture: AsyncClient) -> None:
        payload = {"username": settings.initial_admin_email, "password": "wrongpassword"}
        response = await client_fixture.post("/token", data=payload)

        assert response.status_code == 401
        error_data = response.json()
        assert error_data["detail"] == "incorrect username or password"

    @pytest.mark.anyio
    async def test_login__nonexistent_user(self, client_fixture: AsyncClient) -> None:
        payload = {"username": "nonexistent@email.com", "password": "password"}
        response = await client_fixture.post("/token", data=payload)

        assert response.status_code == 401
        error_data = response.json()
        assert error_data["detail"] == "incorrect username or password"
