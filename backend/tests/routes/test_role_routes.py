import pytest
from httpx import AsyncClient

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.integration
class TestRoleRoutes:
    @pytest.mark.anyio
    async def test_get_role__id_exists(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/roles/1", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == 1
        assert role["name"] == "admin"

    @pytest.mark.anyio
    async def test_get_role__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/roles/100", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_role__not_admin(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.get("/roles/1", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_role__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles/1")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_roles__no_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/roles", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) > 0

    @pytest.mark.anyio
    async def test_get_roles__with_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/roles?name=admin", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) == 1

    @pytest.mark.anyio
    async def test_get_roles__not_admin(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.get("/roles", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_roles__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles")

        assert response.status_code == 401
