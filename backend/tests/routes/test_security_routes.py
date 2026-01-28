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
        assert "refresh_token" in token_data
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

    @pytest.mark.anyio
    async def test_refresh_token__valid_refresh_token(self, client_fixture: AsyncClient) -> None:
        # log in to get a valid refresh token
        login_payload = {"username": settings.initial_admin_email, "password": settings.initial_admin_password}
        login_response = await client_fixture.post("/token", data=login_payload)
        refresh_token = login_response.json()["refresh_token"]

        # use the refresh token to get a new access token
        refresh_payload = {"refresh_token": refresh_token}
        refresh_response = await client_fixture.post("/token/refresh", params=refresh_payload)

        assert refresh_response.status_code == 200
        token_data = refresh_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        assert token_data["refresh_token"] == refresh_token

    @pytest.mark.anyio
    async def test_refresh_token__invalid_refresh_token(self, client_fixture: AsyncClient) -> None:
        refresh_payload = {"refresh_token": "invalidtoken"}
        response = await client_fixture.post("/token/refresh", params=refresh_payload)

        assert response.status_code == 401
        error_data = response.json()
        assert error_data["detail"] == "invalid refresh token"
