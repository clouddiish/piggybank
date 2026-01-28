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
        # log in to get a valid refresh token and set cookies
        login_payload = {"username": settings.initial_admin_email, "password": settings.initial_admin_password}
        login_response = await client_fixture.post("/token", data=login_payload)
        assert login_response.status_code == 200
        cookies = login_response.cookies
        refresh_token = cookies.get("refresh_token")
        assert refresh_token is not None

        # use the refresh token cookie to get a new access token
        refresh_response = await client_fixture.post("/token/refresh", cookies={"refresh_token": refresh_token})

        assert refresh_response.status_code == 200
        token_data = refresh_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        assert token_data["refresh_token"] == refresh_token

    @pytest.mark.anyio
    async def test_refresh_token__invalid_refresh_token(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post("/token/refresh", cookies={"refresh_token": "invalidtoken"})

        assert response.status_code == 401
        error_data = response.json()
        assert error_data["detail"] == "invalid refresh token"

    @pytest.mark.anyio
    async def test_logout(self, client_fixture: AsyncClient) -> None:
        # log in to set cookies
        login_payload = {"username": settings.initial_admin_email, "password": settings.initial_admin_password}
        login_response = await client_fixture.post("/token", data=login_payload)
        assert login_response.status_code == 200
        cookies = login_response.cookies

        logout_response = await client_fixture.post("/token/logout", cookies=cookies)
        assert logout_response.status_code == 200
        data = logout_response.json()
        assert data["detail"] == "Successfully logged out"
