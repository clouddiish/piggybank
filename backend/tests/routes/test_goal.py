import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestGoalRoutes:
    @pytest.mark.anyio
    async def test_get_goal__id_exists(self, client_fixture: AsyncClient, admin_token: str) -> None:
        # create a goal
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "test goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.get("/goals/1", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        goal = response.json()
        assert goal["id"] == 1
        assert goal["type_id"] == 1
        assert goal["name"] == "test goal"
        assert goal["start_date"] == "2025-01-01"
        assert goal["end_date"] == "2025-12-31"
        assert goal["target_value"] == 1000.0
        assert goal["user_id"] == 1

    @pytest.mark.anyio
    async def test_get_goal__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/goals/100", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_goal__different_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "admin goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.get("/goals/1", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_goal__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/goals/1")
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_goals__no_filters_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "admin goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "name": "user goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.get("/goals", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @pytest.mark.anyio
    async def test_get_goals__no_filters_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "admin goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "name": "user goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.get("/goals", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    @pytest.mark.anyio
    async def test_get_goals__with_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "goal1",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "name": "goal2",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.get("/goals?type_id=2", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["type_id"] == 2

    @pytest.mark.anyio
    async def test_get_goals__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/goals")
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_create_goal__all_ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "user goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        assert response.status_code == 201
        goal = response.json()
        assert isinstance(goal["id"], int)
        assert goal["type_id"] == 1
        assert goal["name"] == "user goal"
        assert goal["start_date"] == "2025-01-01"
        assert goal["end_date"] == "2025-12-31"
        assert goal["target_value"] == 1000.0
        assert goal["user_id"] == 2

    @pytest.mark.anyio
    async def test_create_goal__type_not_found(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 100,
                "category_id": None,
                "name": "bad type",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_create_goal__entity_not_associated(self, client_fixture: AsyncClient, user_token: str) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "name": "test category"},
        )

        response = await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 1,
                "category_id": 1,
                "name": "invalid assoc",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        assert response.status_code == 409

    @pytest.mark.anyio
    async def test_create_goal__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post(
            "/goals",
            json={
                "type_id": 1,
                "category_id": None,
                "name": "test goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_update_goal__same_user_ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "before",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.put(
            "/goals/1",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "name": "after",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 2000.0,
            },
        )
        assert response.status_code == 200
        goal = response.json()
        assert goal["type_id"] == 2
        assert goal["name"] == "after"
        assert goal["start_date"] == "2025-01-01"
        assert goal["end_date"] == "2025-12-31"
        assert goal["target_value"] == 2000.0

    @pytest.mark.anyio
    async def test_update_goal__admin_other_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "user goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.put(
            "/goals/1",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "name": "admin edit",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 2000.0,
            },
        )
        assert response.status_code == 200
        goal = response.json()
        assert goal["type_id"] == 2
        assert goal["name"] == "admin edit"
        assert goal["start_date"] == "2025-01-01"
        assert goal["end_date"] == "2025-12-31"
        assert goal["target_value"] == 2000.0

    @pytest.mark.anyio
    async def test_update_goal__different_user_forbidden(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "admin goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.put(
            "/goals/1",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "name": "user edit",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 2000.0,
            },
        )
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_update_goal__id_not_found(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.put(
            "/goals/999",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "test goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_update_goal__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put(
            "/goals/1",
            json={
                "type_id": 1,
                "category_id": None,
                "name": "test goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_delete_goal__same_user_ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "user goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.delete("/goals/1", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        goal = response.json()
        assert goal["id"] == 1
        assert goal["target_value"] == 1000.0

    @pytest.mark.anyio
    async def test_delete_goal__admin_other_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "user goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.delete("/goals/1", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_delete_goal__different_user_forbidden(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/goals",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "name": "admin goal",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "target_value": 1000.0,
            },
        )

        response = await client_fixture.delete("/goals/1", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_delete_goal__id_not_found(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.delete("/goals/999", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_delete_goal__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/goals/1")
        assert response.status_code == 401
