import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestTransactionRoutes:
    @pytest.mark.anyio
    async def test_get_transaction__id_exists(self, client_fixture: AsyncClient, admin_token: str) -> None:
        # create a transaction
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "date": "2025-01-01",
                "value": 100.5,
                "comment": "test transaction",
            },
        )

        response = await client_fixture.get("/transactions/1", headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == 200
        transaction = response.json()
        assert transaction["id"] == 1
        assert transaction["type_id"] == 1
        assert transaction["value"] == 100.5
        assert transaction["user_id"] == 1

    @pytest.mark.anyio
    async def test_get_transaction__id_does_not_exist(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.get("/transactions/100", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_transaction__different_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "date": "2025-01-01",
                "value": 200,
                "comment": "admin transaction",
            },
        )

        response = await client_fixture.get("/transactions/1", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_get_transaction__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/transactions/1")
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_transactions__no_filters_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-02", "value": 50, "comment": "admin transaction"},
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-03", "value": 75, "comment": "user transaction"},
        )

        response = await client_fixture.get("/transactions", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @pytest.mark.anyio
    async def test_get_transactions__no_filters_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-02", "value": 50, "comment": "admin transaction"},
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-03", "value": 75, "comment": "user transaction"},
        )

        response = await client_fixture.get("/transactions", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    @pytest.mark.anyio
    async def test_get_transactions__with_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "date": "2025-01-05",
                "value": 10,
                "comment": "filtered transaction",
            },
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-06", "value": 20, "comment": "other transaction"},
        )

        response = await client_fixture.get(
            "/transactions?type_id=2", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["type_id"] == 2

    @pytest.mark.anyio
    async def test_get_transactions__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/transactions")
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_transactions_total__no_filters_admin(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-02", "value": 50, "comment": "admin transaction"},
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-03", "value": 75, "comment": "user transaction"},
        )

        response = await client_fixture.get("/transactions/total", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 125.0

    @pytest.mark.anyio
    async def test_get_transactions_total__no_filters_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-02", "value": 50, "comment": "admin transaction"},
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-03", "value": 75, "comment": "user transaction"},
        )

        response = await client_fixture.get("/transactions/total", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 75.0

    @pytest.mark.anyio
    async def test_get_transactions_total__with_filters(self, client_fixture: AsyncClient, admin_token: str) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "date": "2025-01-05",
                "value": 10,
                "comment": "filtered transaction",
            },
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-06", "value": 20, "comment": "other transaction"},
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "date": "2025-01-06",
                "value": 30,
                "comment": "another transaction",
            },
        )

        response = await client_fixture.get(
            "/transactions/total?type_id=2", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 50.0

    @pytest.mark.anyio
    async def test_get_transactions_total__no_match_returns_zero(
        self, client_fixture: AsyncClient, admin_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-06", "value": 20, "comment": "other transaction"},
        )
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "type_id": 2,
                "category_id": None,
                "date": "2025-01-06",
                "value": 30,
                "comment": "another transaction",
            },
        )

        response = await client_fixture.get(
            "/transactions/total?type_id=1", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0.0

    @pytest.mark.anyio
    async def test_get_transactions_total__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.get("/transactions/total")
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_create_transaction__all_ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "type_id": 1,
                "category_id": None,
                "date": "2025-01-10",
                "value": 999.9,
                "comment": "new transaction",
            },
        )
        assert response.status_code == 201
        transaction = response.json()
        assert isinstance(transaction["id"], int)
        assert transaction["type_id"] == 1
        assert transaction["value"] == 999.9
        assert transaction["user_id"] == 2

    @pytest.mark.anyio
    async def test_create_transaction__type_not_found(self, client_fixture: AsyncClient, user_token: str) -> None:
        response = await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 100, "category_id": None, "date": "2025-01-10", "value": 20, "comment": "bad type"},
        )
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_create_transaction__entity_not_associated(
        self, client_fixture: AsyncClient, user_token: str
    ) -> None:
        # first create the category
        await client_fixture.post(
            "/categories",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "name": "test category"},
        )

        response = await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "category_id": 1, "date": "2025-01-11", "value": 15, "comment": "invalid assoc"},
        )
        assert response.status_code == 409

    @pytest.mark.anyio
    async def test_create_transaction__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.post(
            "/transactions",
            json={"type_id": 1, "category_id": None, "date": "2025-01-12", "value": 5},
        )
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_update_transaction__same_user_ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-13", "value": 40, "comment": "before"},
        )

        response = await client_fixture.put(
            "/transactions/1",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-13", "value": 60, "comment": "after"},
        )
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["type_id"] == 2
        assert transaction["value"] == 60

    @pytest.mark.anyio
    async def test_update_transaction__admin_other_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-14", "value": 100, "comment": "user transaction"},
        )

        response = await client_fixture.put(
            "/transactions/1",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-14", "value": 200, "comment": "admin edit"},
        )
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["type_id"] == 2
        assert transaction["value"] == 200

    @pytest.mark.anyio
    async def test_update_transaction__different_user_forbidden(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-15", "value": 25, "comment": "admin transaction"},
        )

        response = await client_fixture.put(
            "/transactions/1",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 2, "category_id": None, "date": "2025-01-15", "value": 30},
        )
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_update_transaction__id_not_found(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.put(
            "/transactions/999",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-15", "value": 20},
        )
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_update_transaction__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.put(
            "/transactions/1",
            json={"type_id": 1, "category_id": None, "date": "2025-01-15", "value": 20},
        )
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_delete_transaction__same_user_ok(self, client_fixture: AsyncClient, user_token: str) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-16", "value": 88},
        )

        response = await client_fixture.delete("/transactions/1", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["id"] == 1
        assert transaction["value"] == 88

    @pytest.mark.anyio
    async def test_delete_transaction__admin_other_user(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-17", "value": 77},
        )

        response = await client_fixture.delete("/transactions/1", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_delete_transaction__different_user_forbidden(
        self, client_fixture: AsyncClient, admin_token: str, user_token: str
    ) -> None:
        await client_fixture.post(
            "/transactions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type_id": 1, "category_id": None, "date": "2025-01-18", "value": 66},
        )

        response = await client_fixture.delete("/transactions/1", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_delete_transaction__id_not_found(self, client_fixture: AsyncClient, admin_token: str) -> None:
        response = await client_fixture.delete("/transactions/999", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_delete_transaction__not_logged(self, client_fixture: AsyncClient) -> None:
        response = await client_fixture.delete("/transactions/1")
        assert response.status_code == 401
