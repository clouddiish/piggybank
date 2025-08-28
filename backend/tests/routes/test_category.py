import pytest
from httpx import AsyncClient

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.integration
class TestUserRoutes:
    @pytest.mark.anyio
    async def test_get_category__id_exists(self, client_fixture: AsyncClient, admin_token: str) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "name": "test category"},
        )

        response = await client_fixture.get("/categories/1", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        category = response.json()
        assert category["id"] == 1
        assert category["type_id"] == 1
        assert category["name"] == "test category"
        assert category["user_id"] == 1

    @pytest.mark.anyio
    async def test_get_category__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/categories/100", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_category__different_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        # first create the category as admin user
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "name": "test category"},
        )

        # try to get the category as non-admin user
        response = await client_fixture.get("/categories/1", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_category__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/categories/100")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_categories__no_filters_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        # first create one category as admin user, one as non-admin
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "name": "test admin category"},
        )
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "name": "test user category"},
        )

        response = await client_fixture.get("/categories", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) == 2

    @pytest.mark.anyio
    async def test_get_categories__no_filters_not_an_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        # first create one category as admin user, one as non-admin
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "name": "test admin category"},
        )
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "name": "test user category"},
        )

        response = await client_fixture.get("/categories", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) == 1

    @pytest.mark.anyio
    async def test_get_categories__with_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        # first create the categories
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "name": "test admin category"},
        )
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 2, "name": "test user category"},
        )

        response = await client_fixture.get("/categories?type_id=2", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) == 1

    @pytest.mark.anyio
    async def test_get_categories__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/categories")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_create_category__all_ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "name": "test category"},
        )

        assert response.status_code == 201
        category = response.json()
        assert isinstance(category["id"], int)
        assert category["type_id"] == 1
        assert category["name"] == "test category"
        assert category["user_id"] == 2

    @pytest.mark.anyio
    async def test_create_category__type_not_found(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 100, "name": "test category"},
        )

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_create_category__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post(
            "/categories",
            json={"type_id": 100, "name": "test category"},
        )

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_update_category__all_ok_same_user(self, client_fixture: AsyncClient, user_token: str) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "name": "test category"},
        )

        response = await client_fixture.put(
            "/categories/1",
            json={"type_id": 2, "name": "updated category"},
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 200
        category = response.json()
        assert category["id"] == 1
        assert category["type_id"] == 2
        assert category["name"] == "updated category"
        assert category["user_id"] == 2

    @pytest.mark.anyio
    async def test_update_category__all_ok_different_user_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "name": "test user category"},
        )

        response = await client_fixture.put(
            "/categories/1",
            json={"type_id": 2, "name": "updated category"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        category = response.json()
        assert category["id"] == 1
        assert category["type_id"] == 2
        assert category["name"] == "updated category"
        assert category["user_id"] == 2

    @pytest.mark.anyio
    async def test_update_category__different_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "name": "test user category"},
        )

        response = await client_fixture.put(
            "/categories/1",
            json={"type_id": 2, "name": "updated category"},
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_update_category__category_id_does_not_exist(
        self, client_fixture: AsyncClient, admin_token: str
    ) -> None:
        response = await client_fixture.put(
            "/categories/100",
            json={"type_id": 2, "name": "updated category"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_update_category__type_id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.put(
            "/categories/1",
            json={"type_id": 100, "name": "updated category"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_update_category__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put(
            "/categories/1",
            json={"type_id": 100, "name": "updated category"},
        )

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_delete_category__all_ok_same_user(self, client_fixture: AsyncClient, user_token: str) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "name": "test category"},
        )

        response = await client_fixture.delete(
            "/categories/1",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 200
        category = response.json()
        assert category["id"] == 1
        assert category["type_id"] == 1
        assert category["name"] == "test category"
        assert category["user_id"] == 2

    @pytest.mark.anyio
    async def test_delete_category__all_ok_different_user_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "name": "test category"},
        )

        response = await client_fixture.delete(
            "/categories/1",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        category = response.json()
        assert category["id"] == 1
        assert category["type_id"] == 1
        assert category["name"] == "test category"
        assert category["user_id"] == 2

    @pytest.mark.anyio
    async def test_delete_category__different_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "name": "test category"},
        )

        response = await client_fixture.delete(
            "/categories/1",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_delete_category__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.delete("/categories/100", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_delete_category__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/categories/2")

        assert response.status_code == 401
