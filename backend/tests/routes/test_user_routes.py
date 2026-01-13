import pytest
from httpx import AsyncClient

from app.core.config import get_settings


settings = get_settings()


@pytest.mark.integration
class TestUserRoutes:
    @pytest.mark.anyio
    async def test_get_user_me__ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.get("/users/me", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 200
        user = response.json()
        assert user["id"]
        assert user["role_id"] == 2
        assert user["email"] == "test@email.com"

    @pytest.mark.anyio
    async def test_get_user_me__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/users/me")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_user__id_exists(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/users/1", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 1
        assert user["role_id"]
        assert user["email"] == settings.initial_admin_email

    @pytest.mark.anyio
    async def test_get_user__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/users/100", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_user__not_admin(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.get("/users/100", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_user__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/users/100")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_users__no_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/users", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) > 0

    @pytest.mark.anyio
    async def test_get_users__with_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get(
            f"/users?email={settings.initial_admin_email}", headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 1

    @pytest.mark.anyio
    async def test_get_users__not_admin(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.get("/users", headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_users__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/users")

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_create_user__all_ok(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post("/users", json={"email": "test@email.com", "password": "longpassword123"})

        assert response.status_code == 201
        user = response.json()
        assert isinstance(user["id"], int)
        assert user["role_id"] == 2
        assert user["email"] == "test@email.com"

    @pytest.mark.anyio
    async def test_create_user__password_too_short(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post(
            "/users", json={"role_id": 2, "email": "test@email.com", "password": "short"}
        )

        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_create_user__email_exists(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post(
            "/users", json={"role_id": 2, "email": settings.initial_admin_email, "password": "longpassword123"}
        )

        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_update_user__all_ok_same_user(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.put(
            "/users/2",
            json={
                "role_id": 2,
                "email": "updated@example.com",
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 2
        assert user["role_id"] == 2
        assert user["email"] == "updated@example.com"

    @pytest.mark.anyio
    async def test_update_user__all_ok_different_user_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        response = await client_fixture.put(
            "/users/2",
            json={
                "role_id": 1,
                "email": "updated@example.com",
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 2
        assert user["role_id"] == 1
        assert user["email"] == "updated@example.com"

    @pytest.mark.anyio
    async def test_update_user__all_ok_same_user_cannot_change_role(
        self, client_fixture: AsyncClient, user_token: str
    ) -> None:
        response = await client_fixture.put(
            "/users/2",
            json={
                "role_id": 1,
                "email": "updated@example.com",
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_update_user__different_user(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.put(
            "/users/1",
            json={
                "role_id": 1,
                "email": "updated@example.com",
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_update_user__user_id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.put(
            "/users/100",
            json={
                "role_id": 1,
                "email": "updated@example.com",
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_update_user__role_id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.put(
            "/users/1",
            json={
                "role_id": 100,
                "email": "updated@example.com",
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_update_user__email_exists_different_user(
        self, client_fixture: AsyncClient, admin_token: str
    ) -> None:
        response = await client_fixture.post(
            "/users",
            json={"email": "test@email.com", "password": "longpassword123"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        new_user = response.json()

        response = await client_fixture.put(
            f"/users/{new_user["id"]}",
            json={
                "role_id": 2,
                "email": settings.initial_admin_email,
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_update_user__old_password_wrong(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.put(
            "/users/2",
            json={
                "role_id": 2,
                "email": "test@email.com",
                "old_password": "wrongpassword",
                "new_password": "newpassword",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_update_user__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put(
            "/users/1",
            json={
                "role_id": 1,
                "email": "updated@example.com",
                "old_password": "longpassword123",
                "new_password": "newpassword",
            },
        )

        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_delete_user__all_ok_same_user(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.delete(
            "/users/2",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 2
        assert user["role_id"] == 2
        assert user["email"] == "test@email.com"

    @pytest.mark.anyio
    async def test_delete_user__all_ok_different_user_admin(
        self, client_fixture: AsyncClient, user_token: str, admin_token: str
    ) -> None:
        response = await client_fixture.delete(
            "/users/2",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 2
        assert user["role_id"] == 2
        assert user["email"] == "test@email.com"

    @pytest.mark.anyio
    async def test_delete_user__different_user(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.delete(
            "/users/1",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_delete_user__protected_user(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.delete("/users/1", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_delete_user__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.delete("/users/100", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_delete_user__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/users/2")

        assert response.status_code == 401
