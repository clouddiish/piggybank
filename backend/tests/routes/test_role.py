import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestRoleRoutes:
    @pytest.mark.anyio
    async def test_get_role__id_exists(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles/1")

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == 1
        assert role["name"] == "admin"

    @pytest.mark.anyio
    async def test_get_role__id_does_not_exist(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles/100")

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_roles__no_filters(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles")

        assert response.status_code == 200
        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) > 0

    @pytest.mark.anyio
    async def test_get_roles__with_filters(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles?name=admin")

        assert response.status_code == 200
        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) == 1
