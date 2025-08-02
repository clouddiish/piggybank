import pytest
from httpx import AsyncClient

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.integration
class TestRoleRoutes:
    @pytest.mark.anyio
    async def test_get_by_id__id_exists(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles/1")

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == 1
        assert role["name"] == settings.initial_roles[0]

    @pytest.mark.anyio
    async def test_get_by_id__id_does_not_exist(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles/100")

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_all_with_filters__no_filters(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles")

        assert response.status_code == 200
        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) > 0

    @pytest.mark.anyio
    async def test_get_all_with_filters__with_filters(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles?name=user")

        assert response.status_code == 200
        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) == 1

    @pytest.mark.anyio
    async def test_create__all_ok(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post("/roles", json={"name": "test role"})

        assert response.status_code == 201
        role = response.json()
        assert isinstance(role["id"], int)
        assert role["name"] == "test role"

    @pytest.mark.anyio
    async def test_update__all_ok(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put("/roles/1", json={"name": "updated role"})

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == 1
        assert role["name"] == "updated role"

    @pytest.mark.anyio
    async def test_update__id_does_not_exist(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put("/roles/100", json={"name": "updated role"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_delete__all_ok(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/roles/2")

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == 2
        assert role["name"] == settings.initial_roles[1]

    @pytest.mark.anyio
    async def test_delete__id_does_not_exist(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/roles/100")

        assert response.status_code == 404
