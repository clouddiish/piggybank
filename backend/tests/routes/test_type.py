import pytest
from httpx import AsyncClient

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.integration
class TestTypeRoutes:
    @pytest.mark.anyio
    async def test_get_type__id_exists(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/types/1", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        type = response.json()
        assert type["id"] == 1
        assert type["name"] == "income"

    @pytest.mark.anyio
    async def test_get_type__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/types/100", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_type__not_admin(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.get("/types/1", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_type__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/types/1")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_types__no_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/types", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        types = response.json()
        assert isinstance(types, list)
        assert len(types) > 0

    @pytest.mark.anyio
    async def test_get_types__with_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/types?name=expense", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        types = response.json()
        assert isinstance(types, list)
        assert len(types) == 1

    @pytest.mark.anyio
    async def test_get_types__not_admin(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.get("/types", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_types__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/types")

        assert response.status_code == 401
