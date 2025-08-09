import pytest
from httpx import AsyncClient

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.integration
class TestRoleRoutes:
    @pytest.mark.anyio
    async def test_get_role__id_exists(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/roles/1")

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == 1
        assert role["name"] == settings.initial_roles[0]

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
        response = await client_fixture.get("/roles?name=user")

        assert response.status_code == 200
        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) == 1

    @pytest.mark.anyio
    async def test_create_role__all_ok(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post("/roles", json={"name": "test role"})

        assert response.status_code == 201
        role = response.json()
        assert isinstance(role["id"], int)
        assert role["name"] == "test role"

    @pytest.mark.anyio
    async def test_update_role__all_ok(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put("/roles/1", json={"name": "updated role"})

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == 1
        assert role["name"] == "updated role"

    @pytest.mark.anyio
    async def test_update_role__id_does_not_exist(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put("/roles/100", json={"name": "updated role"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_delete_role__all_ok(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post("/roles", json={"name": "test role"})
        new_role = response.json()
        response = await client_fixture.delete(f"/roles/{new_role["id"]}")

        assert response.status_code == 200
        role = response.json()
        assert role["id"] == new_role["id"]
        assert role["name"] == "test role"

    @pytest.mark.anyio
    async def test_delete_role__protected_role(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/roles/2")

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_delete_role__id_does_not_exist(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/roles/100")

        assert response.status_code == 404
