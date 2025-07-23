import pytest
from httpx import AsyncClient


class TestRoleRoutes:
    @pytest.mark.anyio
    async def test_get_roles__no_filters(self, client_fixture: AsyncClient) -> None:
        print(f"type: {type(client_fixture)}")
        response = await client_fixture.get("/roles")
        assert response.status_code == 200

        roles = response.json()
        assert isinstance(roles, list)
        assert len(roles) > 0
